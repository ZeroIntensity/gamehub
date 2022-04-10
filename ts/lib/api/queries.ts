import { gql } from "./_gql";

export default {
    getComments: gql`
        query getComments($gameName: String!) {
            getGame(name: $gameName) {
                comments {
                    author
                    likes
                    content
                    epoch
                }
            }
        }
    `,
    createPost: gql`
        mutation createPost($title: String!, $content: String!) {
            createPost(data: { title: $title, content: $content }) {
                id
            }
        }
    `,
    userData: gql`
        query getUserData($target: String) {
            userData(target: $target) {
                name
                accountType
            }
        }
    `,
    createComment: gql`
        mutation postComment($gameName: String!, $content: String!) {
            createComment(name: $gameName, content: $content) {
                epoch
                author
                content
            }
        }
    `,
};
