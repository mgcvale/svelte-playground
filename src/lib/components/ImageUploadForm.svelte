<script lang="ts">
    let { images = $bindable([]) } = $props();

    let file: Blob | null = null;
    let errorMsg: string | null = $state(null);

    function handleFileSelection(event: Event): void {
        file = event.target.files[0];
    }

    async function uploadImage(event: Event): Promise<void> {
        event.preventDefault();
        if (file === null) {
            alert("Select a file before trying to upload it!");
            return;
        }
        let formData = new FormData();
        formData.append('image', file);
        await fetch("http://localhost:5000/images/upload", 
            { 
                method: "POST",
                body: formData

            }
        ).then(response => {
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
            errorMsg = null;
        }).catch(error => {
            errorMsg = error;
            console.log(error);
        });
    }
</script>

<div class="upload-form">
    <input type="file" accept="image/*" onchange={handleFileSelection}>
    <button onclick={uploadImage}>Upload image</button>
    {#if errorMsg}
    <p class="error">{errorMsg}</p>
    {/if}
</div>

<style lang="scss">
</style>

