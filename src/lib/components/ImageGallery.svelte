<script lang="ts">
    let { images = $bindable([]) } = $props();

    async function deleteImage(image: string): Promise<void> {
        await fetch(
            "http://localhost:5000/images/delete/" + image, {
                method: "DELETE"
            }
        ).then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok.");
            }
            images = images.filter(item => item !== image);
            return response.json();
        }).then(data => {
            console.log(data);
        }).catch(error => {
            alert("Error: " + error);
        });
    } 
</script>

<div class="image-gallery">
{#each images as image, i}
    <div class="image-card">
        <p>{i+1}</p>
        <img
            src={`http://localhost:5000/images/${image}`}
            alt={image}
        >
        <button onclick={(() => deleteImage(image))}>Delete image</button>
    </div>
{/each}
</div>

<style lang="scss">
    .image-gallery {
        width: min(85%, 1200px);
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;

        .image-card {
            overflow:hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding: 24px;
            width: max(25%, 108px);

            img {
                max-width: 90%;
                max-height: 90%;
                object-fit: contain;
            }

            p {
                font-weight: 500;
                font-size: 1.4em;
                margin: 0;
            }
        }
    }
</style>