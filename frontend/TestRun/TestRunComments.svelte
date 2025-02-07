<script>
    import { onDestroy, onMount } from "svelte";
    import Comment from "../Discussion/Comment.svelte";
    import { userList } from "../Stores/UserlistSubscriber";
    import { sendMessage } from "../Stores/AlertStore";
    import CommentEditor from "../Discussion/CommentEditor.svelte";

    export let id;
    export let releaseName;
    let fetchIntervalId;
    let suppressFetch = false;
    let comments = [];
    let users = {};
    let fetching = false;
    let hideReplyButton = false;
    $: users = $userList;
    const newCommentTemplate = {
        id: "",
        message: "",
        release: releaseName,
        reactions: {},
        mentions: [],
        user_id: "",
        release_id: "",
        test_run_id: id,
        posted_at: new Date(),
    };

    let newCommentBody = Object.assign({}, newCommentTemplate);

    const fetchComments = async function () {
        try {
            let params = new URLSearchParams({
                testId: id,
            }).toString();
            let apiResponse = await fetch("/api/v1/test_run/comments?" + params);
            let apiJson = await apiResponse.json();
            if (apiJson.status === "ok") {
                comments = apiJson.response;
            } else {
                throw apiJson;
            }
        } catch (error) {
            if (error?.status === "error") {
                sendMessage(
                    "error",
                    `Unable to fetch comments.\nMessage: ${error.response.arguments[0]}`
                );
            } else {
                sendMessage(
                    "error",
                    "A backend error occurred during comments fetch"
                );
            }
        }
    };

    const handleCommentSubmit = async function (e) {
        let commentBody = e.detail;
        fetching = true;
        try {
            let apiResponse = await fetch("/api/v1/test_run/comments/submit", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(commentBody),
            });
            let apiJson = await apiResponse.json();
            console.log(apiJson);
            if (apiJson.status === "ok") {
                comments = apiJson.response;
                fetching = false;
            } else {
                throw apiJson;
            }
        } catch (error) {
            if (error?.status === "error") {
                sendMessage(
                    "error",
                    `API Error during comment submission.\nMessage: ${error.response.arguments[0]}`
                );
            } else {
                sendMessage(
                    "error",
                    "A backend error occurred during comment submission"
                );
            }
        } finally {
            newCommentBody = Object.assign({}, newCommentTemplate);
        }
    };

    const handleCommentUpdate = async function (e) {
        let commentBody = e.detail;
        suppressFetch = false;
        try {
            let apiResponse = await fetch("/api/v1/test_run/comments/update", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(commentBody),
            });
            let apiJson = await apiResponse.json();
            console.log(apiJson);
            if (apiJson.status === "ok") {
                comments = apiJson.response;
            } else {
                throw apiJson;
            }
        } catch (error) {
            if (error?.status === "error") {
                sendMessage(
                    "error",
                    `API Error during comment update.\nMessage: ${error.response.arguments[0]}`
                );
            } else {
                sendMessage(
                    "error",
                    "A backend error occurred during comment update."
                );
            }
        }
    };

    const handleCommentReply = function (e) {
        let author_id = e.detail.author;
        let author = users?.[author_id]?.username;
        let quotedMessage = e.detail.message.trim().split("\n").map((val) => `> ${val}`).join("\n");
        newCommentBody.message = `${author ? `@${author} posted:` : ""}${newCommentBody.message}\n${quotedMessage}\n`;
    };

    const handleCommentDelete = async function (e) {
        let commentBody = e.detail;
        try {
            let apiResponse = await fetch("/api/v1/test_run/comments/delete", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(commentBody),
            });
            let apiJson = await apiResponse.json();
            console.log(apiJson);
            if (apiJson.status === "ok") {
                comments = apiJson.response;
            } else {
                throw apiJson;
            }
        } catch (error) {
            if (error?.status === "error") {
                sendMessage(
                    "error",
                    `API Error during comment deletion.\nMessage: ${error.response.arguments[0]}`
                );
            } else {
                sendMessage(
                    "error",
                    "A backend error occurred during release comment deletion."
                );
            }
        }
    };

    onMount(() => {
        fetchComments();
        fetchIntervalId = setInterval(() => {
            if (suppressFetch) return;
            fetchComments();
        }, 60 * 1000);
    });

    onDestroy(() => {
        clearInterval(fetchIntervalId);
    });
</script>

<div class="container-fluid bg-editor">
    {#if Object.keys(users).length > 0}
        {#each comments as comment (comment.id)}
            <div class="row">
                <div class="col my-3">
                    <Comment
                        commentBody={comment}
                        {users}
                        {hideReplyButton}
                        on:commentDelete={handleCommentDelete}
                        on:commentUpdated={handleCommentUpdate}
                        on:commentEditing={() => (suppressFetch = true)}
                        on:commentReply={handleCommentReply}
                    />
                </div>
            </div>
        {:else}
            <div class="row">
                <div class="col text-center p-1 text-muted">
                    No comments yet.
                </div>
            </div>
        {/each}
    {:else}
        <div class="col m-1">
            <div class="text-muted text-center p-2 fs-4">
                <span class="spinner-grow" /> Loading...
            </div>
        </div>
    {/if}
    <div class="row border-top">
        {#if !fetching}
            <div class="col mx-1 my-2">
                <CommentEditor
                    runId={id}
                    mode="post"
                    bind:commentBody={newCommentBody}
                    on:submitComment={handleCommentSubmit}
                />
            </div>
        {:else}
            <div class="col m-1">
                <div class="text-muted text-center p-2 fs-4">
                    <span class="spinner-grow" /> Loading...
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .img-profile {
        height: 72px;
        border-radius: 50%;
        object-fit: cover;
    }

    .bg-editor {
        background-color: #f2f2f2;
    }
</style>
