<script lang="ts">
    import { CONFIG } from "../../config";

    let { images = $bindable([]) } = $props();

    let files: [Blob] | null = null;
    let infoMsg: string | null = $state(null);

    function handleFileSelection(event: Event): void {
        if (event.target == null) {
            files = null;
            return;
        }
        files = event.target.files;
    }

    async function uploadImage(event: Event): Promise<void> {
        event.preventDefault();
        if (files == null) {
            alert("Select a file before trying to upload it!");
            return;
        }

        let errorCount = 0;

        for (let i = 0; i < files.length; i++) {
            infoMsg = "Uploading image " + (i+1) + " of " + files.length;
            let formData = new FormData();
            formData.append('image', files[i]);
            await fetch(CONFIG.getApiUrl("images/upload"), 
                { 
                    method: "POST",
                    body: formData
                }
            ).then(response => {
                console.log("Response Recieved");
                if (!response.ok) {
                    throw new Error("Response not ok when uploading file");
                }
                return response.json();
            }).then(json => {
                let filename: String = json.filename;
                console.log(filename);
                if (filename == null) {
                    throw new Error("Malformed response form server");
                }
                images.push(filename);
            }).catch(error => {
                errorCount++;
                console.log(error);
            });
        }

        if (errorCount > 0) {
            infoMsg = "Error uploading " + errorCount + (errorCount > 1) ? "images" : "image" + " of " + files.length;
        } else {
            infoMsg = "Uploaded " + files.length + " Images!";
        }

        setTimeout(() => {
            infoMsg = null;
        }, 3000)
    }
</script>

<div class="upload-form">
    <input type="file" accept="image/*" multiple onchange={handleFileSelection}>
    <button onclick={uploadImage}>Upload image</button>
    {#if infoMsg}
    <p class="error">{infoMsg}</p>
    {/if}
</div>

<style lang="scss">
    * {
        display: inline;
    }

    p {
        padding: 0 2em;
    }
</style>

