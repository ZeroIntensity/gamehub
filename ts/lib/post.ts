import post from "./api/wrappers/createPost";

export async function createPost(
    title: string,
    content: string
): Promise<string> {
    const response = await post(title, content);

    if (response.errors) {
    }

    return response.data!.createPost.id;
}
