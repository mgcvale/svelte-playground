<script lang="ts">
	import ImageGallery from "$lib/components/ImageGallery.svelte";
	import ImageUploadForm from "$lib/components/ImageUploadForm.svelte";
	import { onMount } from "svelte";
    import { CONFIG } from "../config";

    let images: string[] = $state([]);

    onMount(() => {
        fetch (CONFIG.getApiUrl("images/all"), {
            method: "GET"
        }).then(response => {
            if (!response.ok) {
                throw new Error("Error gathering all images");
            }
            return response.json();
        }).then(json => {
            console.log(json);
            images = json.images;
            if (images == null) {
                images = [];
            }
        }).catch(error => {
            alert("Error loading images from server!");
        });
    });

</script>

<main>
    <h1>Image upload website</h1>
    <ImageUploadForm bind:images={images}></ImageUploadForm>
    <ImageGallery bind:images={images}></ImageGallery>
</main>

<style lang="scss">
    main {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
</style>
