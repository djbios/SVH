<template>
        <v-container >
            <v-btn v-bind:to="'/'+((folder.parent==null) ? folder.id : folder.parent).toString()">{{folder.name}}</v-btn>
            <v-row align="center">
                <v-col
                        v-for="child in folder.children"
                        :key="child.id"
                        cols="12"
                        sm="4"
                >
                    <v-card v-bind:to="'/'+child.id.toString()"
                         supportingtext="true"  image="true" style="height: 400px; min-width: 150px">
                        <div class="d-flex align-center justify-center v-sheet theme--light grey lighten-3"
                             style="height: 200px;"><i aria-hidden="true"
                                                       class="v-icon notranslate mdi mdi-image theme--light"
                                                       style="font-size: 64px;"></i></div>
                        <div class="v-card__title">
                            {{child.name}}
                        </div>
                        <div class="v-card__subtitle"></div>
                        <div class="v-card__text">
                            {{child.description}}
                        </div>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>


</template>

<script>
    import axios from 'axios'
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

    export default {
        name: "FoldersGrid",
        data() {
            return {
                folder: {}
            }
        },
        mounted() {
            this.load_folder(this.$route.params['folder_id'])
        },
        watch: {
            $route(to) {
                console.log(to)
                this.load_folder(to.params['folder_id'])
            }
        },
        methods: {
            load_folder(id) {
                if (id == null){
                    id = 'root'
                }
                axios.get('http://localhost:8000/videofolder/'+id+'/')
                    .then(response => (this.folder = response.data))
            }
        }
    }
</script>

<style scoped>

</style>