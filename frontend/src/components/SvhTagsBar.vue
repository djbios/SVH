<template>
   
</template>

<script>
    export default {
        name: "SvhTagsBar",
        vars: {},
        data () {
        },
        mounted() {
            axios
                .get('https://api.coindesk.com/v1/bpi/currentprice.json')
                .then(response => (this.js = response.data.bpi.USD));
        }
    }

</script>

<style scoped>

</style>