<script>
    import { createEventDispatcher } from "svelte";
    import * as urlSlug from "url-slug";
    export let groups = [];
    export let releaseId = "";
    export let groupId = "";
    const dispatch = createEventDispatcher();
    let newTest = {
        test_name: "",
        pretty_name: "",
        group_id: groupId,
        build_id: "",
        build_url: "",

    };
    $: newTest.test_name = urlSlug.convert(newTest.pretty_name);

    const handleTestCreate = function() {
        dispatch("testCreate", Object.assign({
            release_id: releaseId,
            group_id: groupId,
        }, newTest));
    };

    const handleTestCreationCancel = function() {
        dispatch("testCreateCancel");
    };
</script>

<div class="position-fixed popup-test-creator">
    <div class="row h-100 justify-content-center align-items-center">
        <div class="col-5 rounded bg-white shadow-sm p-2">
            <div class="form-group">
                <label for="" class="form-label">New test name</label>
                <input
                    type="text"
                    class="form-control"
                    disabled
                    bind:value={newTest.test_name}
                />
            </div>
            <div class="form-group">
                <label for="" class="form-label">Friendly name</label>
                <input
                    type="text"
                    class="form-control"
                    bind:value={newTest.pretty_name}
                />
            </div>
            <div class="form-group">
                <label for="" class="form-label">Build System Id</label>
                <input
                    type="text"
                    class="form-control"
                    bind:value={newTest.build_id}
                />
            </div>
            <div class="form-group">
                <label for="" class="form-label">Build System URL (Optional)</label>
                <input
                    type="text"
                    class="form-control"
                    bind:value={newTest.build_url}
                />
            </div>
            <div class="form-group mb-2">
                <label for="" class="form-label">Target group</label>
                <select id="" class="form-select" bind:value={newTest.group_id}>
                    {#each groups as group}
                        <option value={group.id}
                            >{group.pretty_name || group.name}</option
                        >
                    {/each}
                </select>
            </div>
            <div class="mt-2 text-end">
                <button
                    class="btn btn-secondary"
                    on:click={handleTestCreationCancel}
                >
                    Cancel
                </button>
                <button class="btn btn-success" on:click={handleTestCreate}>
                    Create
                </button>
            </div>
        </div>
    </div>
</div>

<style>
    .popup-test-creator {
        background-color: rgba(0, 0, 0, 0.5);
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 999;
    }
</style>
