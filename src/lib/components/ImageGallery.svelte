<script lang="ts">
    let { images = $bindable([]) } = $props();

    async function deleteImage(image: string): Promise<void> {
        await fetch(
            "https://svelte-playground-production.up.railway.app/images/delete/" + image, {
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

<section class="image-gallery">
{#each images as image, i}
    <div class="image-card">
        <p>{i+1}</p>
        <a href={`https://svelte-playground-production.up.railway.app/images/${image}`} target="_blank">
            <img
                src={`https://svelte-playground-production.up.railway.app/images/${image}`}
                alt={image}
            >
        </a>
        <button onclick={(() => deleteImage(image))}>Delete image</button>
    </div>
{/each}
</section>

<style lang="scss">
    .image-gallery {
        width: min(85%, 1200px);
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
        justify-content: center;

        .image-card {
            overflow:hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding: 24px;
            width: max(25%, 330px);

            font-size: 1.4em;

            a {
                display: flex;
                align-items: center;
                justify-content: center;
            }

            img {
                width: 100%;
                height: 20vh;
                object-fit: cover;
                border-radius: 8px;
                transition: 250ms;

                &:hover {
                    transform: scale(1.04);
                }
            }

            button {
                transition: 250ms;
                &:hover {
                    transform: scale(1.06);
                }
            }

            p {
                font-weight: 500;
                margin: 0;
            }
        }
    }
</style>