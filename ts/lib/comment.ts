import createComment from "./api/wrappers/postComment";

export default async (gameName: string, content: string) => {
    const response = await createComment(gameName, content);

    return response;
};
