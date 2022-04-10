import gql from "../_gql";
import makeRequest from "../makeRequest";

const query = gql`
    query commentsForGame($gameName: String!) {
        getGame(name: $gameName) {
            comments {
                epoch
                author
                likes
                content
            }
        }
    }
`;

export default async (
    gameName: string
): APIResponse<{
    getGame: {
        comments: Array<{
            epoch: number;
            author: string;
            likes: Array<string>;
            content: string;
        }>;
    };
}> => {
    return makeRequest(query, { gameName });
};
