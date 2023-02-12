<template>
<q-layout>
  <q-header class="bg-dark">
          <q-toolbar>
            <q-toolbar-title>Transaction</q-toolbar-title>
          </q-toolbar>
        </q-header>
  <q-toolbar-title>Apriori Model</q-toolbar-title>
  <q-page-container>
    <q-page>
   

</q-page>
</q-page-container>
</q-layout>
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
