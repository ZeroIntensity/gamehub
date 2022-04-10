import post from "./api/wrappers/createPost";
import handleErrors from "./utils/handleErrors";

export async function createPost(
    title: string,
    content: string
): Promise<WrapperResponse> {
    return handleErrors(await post(content, title));
}
