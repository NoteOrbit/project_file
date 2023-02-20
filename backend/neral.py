import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.functional as F
from itertools import product
import pickle

"""

read data to init data 
and clean data duplicates and nan data

"""

df = pd.read_csv('data/real.csv')
df = df.iloc[0:,[1,2,3]]
# df = df.drop_duplicates(['Store',"User"]) if use set len shape data pivot
# df = df.dropna()


"""

Create Functions use device

"""


def get_device() -> str:
    """
    Returns the device that available for use. 
    Priority:  GPU (CUDA) > M1 (MPS) > CPU
    
    Returns:
        string of device name
    """
    
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps"):
        if torch.backends.mps.is_available() and torch.backends.mps.is_built():
            return "mps"
    return "cpu"



"""

Create VanillaMF model base

"""


class VanillaMF(nn.Module):
    """
    An implementation of vanilla matrix factorization model.
    """
    
    def __init__(self, n_users: int, n_items: int, latent_dim: int = 10):
        super().__init__()
        
        self.user_embeddings = nn.Embedding(n_users, latent_dim)
        self.item_embeddings = nn.Embedding(n_items, latent_dim)
        
        self.user_h1 = nn.Linear(latent_dim, latent_dim // 2) ## linear layer
        self.item_h1 = nn.Linear(latent_dim, latent_dim // 2) ## linear layer
        

        
        # self.user_h1_dropout = nn.Dropout(0.25)
        # self.item_h1_dropout = nn.Dropout(0.25)
        
    def forward(self, user_ids: torch.Tensor, item_ids: torch.Tensor) -> torch.Tensor:
        user_emb = self.user_embeddings(user_ids).squeeze(dim=1)  # (batch_size, latent_dim)
        item_emb = self.item_embeddings(item_ids).squeeze(dim=1)  # (batch_size, latent_dim)
        
        user_h1 = self.user_h1(user_emb)
        item_h1 = self.user_h1(item_emb)
        
        
        
#         user_h1 = self.user_h1_dropout(user_h1)
#         item_h1 = self.item_h1_dropout(user_h1)
        
        dot_product = torch.sum(user_h1 * item_h1, dim=1)
        
        # return (user_h1 * item_h1).sum(dim=1)  # (batch_size, )
        # output = relu(dot_product)
        return dot_product

    def loss_fn(self, preds: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Simple MSE loss as the loss function for the model.
        
        Args:
            preds: predicted scores
            targets: ground truth scores
            
        Returns:
            MSE of the predictions and the ground truth
        """
        
        # return nn.MSELoss()(preds, targets)  # use package to calculate loss
        return ((preds - targets) ** 2).mean()

"""

Create options model RegularizedMF

"""

class RegularizedMF(VanillaMF):
    """
    Regularized matrix factorization model.
    
    References:
        - https://developers.google.com/machine-learning/recommendation/collaborative/matrix
        - https://colab.research.google.com/github/google/eng-edu/blob/main/ml/recommendation-systems/recommendation-systems.ipynb
    """
    
    def __init__(self, 
                 n_users: int, 
                 n_items: int, 
                 latent_dim: int = 10,
                 reg_coef: float = 0.1,
                 gravity_coeff: float = 1.):
        super().__init__(n_users, n_items, latent_dim)
        
        self.reg_coef = reg_coef
        self.gravity_coeff = gravity_coeff
    
    def regularization_loss(self) -> torch.Tensor:
        """
        Calculate the regularization loss.
        
        Returns:
            regularization loss
        """
        
        user_reg_loss = self.user_embeddings.weight.norm(p=2, dim=1).mean()
        item_reg_loss = self.item_embeddings.weight.norm(p=2, dim=1).mean()
        
        return self.reg_coef * (user_reg_loss + item_reg_loss)
    
    def gravity_loss(self) -> torch.Tensor:
        """
        Calculate the gravity loss.
        
        Returns:
            gravity loss
        """
        
        user_emb = self.user_embeddings.weight  # (n_users, latent_dim)
        item_emb = self.item_embeddings.weight  # (n_items, latent_dim)
        
        denominator = (user_emb.shape[0] * item_emb.shape[0]) * ((user_emb.T @ user_emb) * (item_emb.T @ item_emb)).sum()
        
        return self.gravity_coeff * 1 / denominator

    def loss_fn(self, preds: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        MSE loss with regularization.
        
        Args:
            preds: predicted scores
            targets: ground truth scores
            
        Returns:
            MSE of the predictions and the ground truth
        """
        
        return super().loss_fn(preds, targets) + self.regularization_loss() + self.gravity_loss()







"""

setup data to model vanilaMF

"""

data = df.copy()

device = get_device() ## setup device use 

## take indice user and item for ref data to original
user2idx = {user: idx for idx, user in enumerate(data.User.unique())} 
idx2user = {idx: user for user, idx in user2idx.items()}

item2idx = {item: idx for idx, item in enumerate(data.Store.unique())}
idx2item = {idx: item for item, idx in item2idx.items()}




## setup to encodeddata to map with indice
encoded_df = data.copy()

encoded_df["User"] = encoded_df["User"].map(user2idx)
encoded_df["Store"] = encoded_df["Store"].map(item2idx)


## after data to convert str to int indice 
pd.pivot_table(encoded_df, values='Rating', index='User', columns='Store')



'''

setup model

'''

N_EPOCH = 30
BATCH_SIZE = 512
LEARNING_RATE = 0.02
LATENT_DIM = 15


"""

cretae dataloader with dataloder lib

"""

class CustomDataset(Dataset):
    def __init__(self, df):
        self.df = df
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        user_id = self.df.iloc[idx].User
        item_id = self.df.iloc[idx].Store
        rating = self.df.iloc[idx].Rating
        
        return user_id.astype("int"), item_id.astype("int"), rating.astype("float32")


"""

split data to model with class CustomDataset or Dataloader

"""

# Train test split
train_df = encoded_df.copy().sample(frac=0.6, random_state=1)
test_df = encoded_df.copy().drop(train_df.index)

# Create dataloader
train_loader = DataLoader(
    CustomDataset(train_df.copy()),
    batch_size=BATCH_SIZE,
    shuffle=True,
)

test_loader = DataLoader(
    CustomDataset(test_df.copy()),
    batch_size=test_df.shape[0],
)



"""

set up model with RegularizedMF

"""

model = RegularizedMF(
    n_users=2237, 
    n_items=33,
    latent_dim=LATENT_DIM
).to(get_device())

opt = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE) ## optim by adam



'''

train model

'''



loss_hist = []
eval_loss_hist = []

for epoch in range(0, N_EPOCH):
    for i, (user_ids, item_ids, ratings) in enumerate(train_loader):
        user_ids = user_ids.to(device)
        item_ids = item_ids.to(device)
        ratings = ratings.to(device)
        
        # training
        _ = model.train()
        opt.zero_grad()
        
        pred_scores = model(user_ids, item_ids)
        loss = model.loss_fn(pred_scores, ratings)
        
        loss.backward()
        opt.step()
        
        # evaluation
        _ = model.eval()
        
        with torch.no_grad():
            eval_loss = 0
            for j, (user_ids, item_ids, ratings) in enumerate(test_loader):
                user_ids = user_ids.to(device)
                item_ids = item_ids.to(device)
                ratings = ratings.to(device)
                
                pred_scores = model(user_ids, item_ids)
                eval_loss += model.loss_fn(pred_scores, ratings)
                
            eval_loss /= len(test_loader)
        
        loss_hist.append(loss.item())
        eval_loss_hist.append(eval_loss.item())
        
    if epoch % 1 == 0:
        print(f"Epoch: {epoch}, Loss: {loss.item():.4f}, Eval Loss: {eval_loss.item():.4f}")




'''

model to data pd

'''

user_item_pair = list(product(range(2237), range(33)))
user_item_pair = np.array(user_item_pair)



_ = model.eval()

# Predict scores for all user-item pairs
user_ids = torch.IntTensor(user_item_pair[:, 0].copy()).to(device)
item_ids = torch.IntTensor(user_item_pair[:, 1].copy()).to(device)

pred = model(
    user_ids,
    item_ids
)

user_item_score = pd.DataFrame(user_item_pair.copy(), columns=["User", "Store"])
user_item_score["pred"] = pred.cpu().detach().numpy()



result = pd.pivot_table(user_item_score, values='pred', index='User', columns='Store').round(1)



file = open('data.csv','wb')
pickle.dump(result,file)
file.close

