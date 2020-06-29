<template>
        <v-container >
            <v-row align="center">
                <v-col
                        v-for="child in videos"
                        :key="child.id"
                        cols="12"
                        sm="4"
                >
                    <v-card
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
                videos: []
            }
        },
        mounted() {
            this.load_videos(this.$route.params['folder_id'])
        },
        watch: {
            $route(to) {
                this.load_videos(to.params['folder_id'])
            }
        },
        methods: {
            load_videos(id) {
                if (id != null) {
                    axios.get('http://localhost:8000/videofile/?folder=' + id)
                        .then(response => (this.videos = response.data))
                }
            }
        }
    }
</script>

<style scoped>

</style>