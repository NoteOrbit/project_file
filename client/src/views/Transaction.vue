<template>
  <div class="container-lg my-2">
    <q-card bordered :style="{ height: '400px' }" horizontal>
    <q-card-section>
      <q-row>
        <q-col sm="4" class="text-center">
          <p class="title">Likes</p>
          <p class="value">{{ likes }}</p>
        </q-col>
        <q-col sm="4" class="text-center">
          <p class="title">Views</p>
          <p class="value">{{ views }}</p>
        </q-col>
        <q-col sm="4" class="text-center">
          <p class="title">Transactions</p>
          <p class="value">{{ transactions }}</p>
        </q-col>
      </q-row>
    </q-card-section>
    <q-card-section>
      <q-table
        :data="transactionsList"
        :columns="tableColumns"
        row-key="transactionId"
      />
    </q-card-section>
  </q-card>
</div>
</template>

<script>
export default {
  data() {
    return {
      likes: 20,
      views: 30,
      transactions: 40,
      transactionsList: [
      ],
      tableColumns: [
        {
          name: "Transaction ID",
          field: "transactionId",
          sortable: true
        },
        {
          name: "Date",
          field: "date",
          sortable: true
        },
        {
          name: "Amount",
          field: "amount",
          sortable: true
        }
      ]
    };
  },
  created() {
    // Fetch the data for likes, views, transactions, and transactionsList from the API
  }
};
</script>
