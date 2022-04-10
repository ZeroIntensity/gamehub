import commentsForGame from "./api/wrappers/commentsForGame";
import handleAllErrors from "./utils/handleAllErrors";

export default async (name: string) => {
    const response = await commentsForGame(name);
    handleAllErrors(response);

    return response.json.data!.getGame.comments;
};
