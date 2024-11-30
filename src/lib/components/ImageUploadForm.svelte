<script lang="ts">
    let { images = $bindable([]) } = $props();

    let file: Blob | null = null;
    let infoMsg: string | null = $state(null);

    function handleFileSelection(event: Event): void {
        file = event.target.files[0];
    }

    async function uploadImage(event: Event): Promise<void> {
        infoMsg = "Uploading image...";
        event.preventDefault();
        if (file === null) {
            alert("Select a file before trying to upload it!");
            return;
        }
        let formData = new FormData();
        formData.append('image', file);
        await fetch("https://svelte-playground-production.up.railway.app/images/upload", 
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
            infoMsg = "Image uploaded!"; setTimeout(() => {
                infoMsg = null;
            }, 3000)
        }).catch(error => {
            infoMsg = "Error uploading image!";
            setTimeout(() => {
                infoMsg = null;
            }, 3000)
            console.log(error);
        });
    }
</script>

<div class="upload-form">
    <input type="file" accept="image/*" onchange={handleFileSelection}>
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

