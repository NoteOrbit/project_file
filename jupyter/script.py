import pandas as pd
import numyp as np
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from itertools import product


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


class VanillaMF(nn.Module):
    """
    An implementation of vanilla matrix factorization model.
    """

    def __init__(self, n_users: int, n_items: int, latent_dim: int = 10):
        super().__init__()

        self.user_embeddings = nn.Embedding(n_users, latent_dim)
        self.item_embeddings = nn.Embedding(n_items, latent_dim)

        self.user_h1 = nn.Linear(latent_dim, latent_dim // 2)
        self.item_h1 = nn.Linear(latent_dim, latent_dim // 2)

        self.user_h1_dropout = nn.Dropout(0.25)
        self.item_h1_dropout = nn.Dropout(0.25)

    def forward(self, user_ids: torch.Tensor, item_ids: torch.Tensor) -> torch.Tensor:
        user_emb = self.user_embeddings(user_ids).squeeze(
            dim=1)  # (batch_size, latent_dim)
        item_emb = self.item_embeddings(item_ids).squeeze(
            dim=1)  # (batch_size, latent_dim)

        user_h1 = self.user_h1(user_emb)
        item_h1 = self.user_h1(item_emb)

        user_h1 = self.user_h1_dropout(user_h1)
        item_h1 = self.item_h1_dropout(user_h1)

        return (user_h1 * item_h1).sum(dim=1)  # (batch_size, )

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

        denominator = (user_emb.shape[0] * item_emb.shape[0]) * \
            ((user_emb.T @ user_emb) * (item_emb.T @ item_emb)).sum()

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


class sc():
    def __init__(self,
                 N_EPOCH=20,
                 BATCH_SIZE=521,
                 LEARNING_RATE=0.02,
                 LATENT_DIM=3,
                 ):

        self.N_EPOCH = N_EPOCH
        self.BATCH_SIZE = BATCH_SIZE
        self.LEARNING_RATE = LEARNING_RATE
        self.LATENT_DIM = LATENT_DIM

    def setup_data(self, data):

        user2idx = {user: idx for idx, user in enumerate(data.User.unique())}
        idx2user = {idx: user for user, idx in user2idx.items()}

        item2idx = {item: idx for idx, item in enumerate(data.Store.unique())}
        idx2item = {idx: item for item, idx in item2idx.items()}

        encoded_df = data.copy()

        encoded_df["User"] = encoded_df["User"].map(user2idx)
        encoded_df["Store"] = encoded_df["Store"].map(item2idx)

        # Train test split
        train_df = encoded_df.copy().sample(frac=0.6, random_state=1)
        test_df = encoded_df.copy().drop(train_df.index)

        # Create dataloader
        train_loader = DataLoader(
            CustomDataset(train_df.copy()),
            batch_size=self.BATCH_SIZE,
            shuffle=True,
        )

        test_loader = DataLoader(
            CustomDataset(test_df.copy()),
            batch_size=test_df.shape[0],
        )


class model(sc):
    def __init__(self, n_users, n_itmes):
        super().__init__()
        self.n_users = n_users
        self.n_itmes = n_itmes

    def model_setup(self):
        model = RegularizedMF(
            n_users=2237,
            n_items=33,
            latent_dim=self.LATENT_DIM
        ).to(get_device())
        opt = torch.optim.Adam(model.parameters(), lr=self.LEARNING_RATE)
        loss_hist = []
        eval_loss_hist = []

        for epoch in range(0, self.N_EPOCH):
            for i, (user_ids, item_ids, ratings) in enumerate(train_loader):
                user_ids = user_ids.to(get_device())
                item_ids = item_ids.to(get_device())
                ratings = ratings.to(get_device())

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
                        user_ids = user_ids.to(get_device())
                        item_ids = item_ids.to(get_device())
                        ratings = ratings.to(get_device())

                        pred_scores = model(user_ids, item_ids)
                        eval_loss += model.loss_fn(pred_scores, ratings)

                    eval_loss /= len(test_loader)

                loss_hist.append(loss.item())
                eval_loss_hist.append(eval_loss.item())

            if epoch % 1 == 0:
                print(
                    f"Epoch: {epoch}, Loss: {loss.item():.4f}, Eval Loss: {eval_loss.item():.4f}")


# user2idx = {user: idx for idx, user in enumerate(data.User.unique())}
# idx2user = {idx: user for user, idx in user2idx.items()}

# item2idx = {item: idx for idx, item in enumerate(data.Store.unique())}
# idx2item = {idx: item for item, idx in item2idx.items()}


# N_EPOCH = 20
# BATCH_SIZE = 521
# LEARNING_RATE = 0.02
# LATENT_DIM = 3


if __name__ == "__main__":
    sc()
