import { gql } from "./_gql";

export default {
	getComments: gql`
		query getComments($gameName: String!) {
			getGame(name: $gameName) {
				comments {
					author
					content
					epoch
					accountType
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
				accountType
			}
		}
	`,
	likeGame: gql`
		mutation likeGame($gameName: String!) {
			likeGame(name: $gameName)
		}
	`,
	unlikeGame: gql`
		mutation unlikeGame($gameName: String!) {
			unlikeGame(name: $gameName)
		}
	`,
	createAccount: gql`
		mutation createAccount($username: String!, $password: String!) {
			createAccount(credentials: { name: $username, password: $password })
		}
	`,
	login: gql`
		mutation login($username: String!, $password: String!) {
			login(credentials: { name: $username, password: $password })
		}
	`,
	userReport: gql`
		mutation userReport($target: String!, $content: String!) {
			userReport(content: $content, target: $target)
		}
	`,
	deleteAccount: gql`
		mutation deleteAccount($target: String) {
			deleteAccount(target: $target)
		}
	`,

	promoteAccount: gql`
		mutation promoteAccount($target: String!) {
			promote(username: $target)
		}
	`,

	demoteAccount: gql`
		mutation demoteAccount($target: String!) {
			demote(username: $target)
		}
	`,

	deleteGame: gql`
		mutation deleteGame($target: String!) {
			deleteGame(name: $target)
		}
	`,

	apply: gql`
		mutation apply(
			$discordTag: String!
			$questionOne: Boolean!
			$questionTwo: Boolean!
			$anyOtherHelp: String
		) {
			apply(
				content: {
					discordTag: $discordTag
					questionOne: $questionOne
					questionTwo: $questionTwo
					anyOtherHelp: $anyOtherHelp
				}
			)
		}
	`,
};
