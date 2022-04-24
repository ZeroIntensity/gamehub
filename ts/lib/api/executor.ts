import makeRequest from "./makeRequest";
import cookies, { isAuthenticated } from "../cookies";
import queries from "./queries";
import { Query } from "./_gql";

export class GraphQLExecutor {
	private _authorization?: string;

	constructor(authKey?: string) {
		this._authorization = authKey;
	}

	public async dispatch<T extends {}>(
		query: Query,
		variables: Variables
	): Promise<GraphQLResponse<T>> {
		try {
			return (await makeRequest(
				query.raw,
				variables,
				this._authorization
			)) as GraphQLResponse<T>;
		} catch (e) {
			throw new Error(`GraphQL request failed: ${e}`);
		}
	}

	public merge(a: Query, b: Query, namestr: string) {
		return new Query(`mutation ${namestr} {
${a.body}
${b.body}
}`);
	}

	public set setAuthKey(key: string) {
		this._authorization = key;
	}
}

export class GraphQLClient {
	private executor: GraphQLExecutor;

	constructor() {
		this.executor = new GraphQLExecutor(
			isAuthenticated ? cookies.auth : undefined
		);
	}

	private finalizeResponse<T>(response: GraphQLResponse<T>) {
		const errors = response.json.errors;

		if (response.status != 200) {
			// case for a validation error
			return {
				ok: false,
				response,
				message: errors![0].message,
			};
		}

		if (errors && response.status == 200) {
			// case for a server error
			if (errors.length > 1) {
				errors.forEach(err => console.error(`GraphQL error: ${err.message}`));
				throw new Error("GraphQL request failed");
			} else throw new Error(`GraphQL request failed: ${errors[0].message}`);
		}

		return {
			ok: true,
			response,
		};
	}

	private async executeQuery<T>(
		query: Query,
		variables: Variables
	): Promise<APIResponse<T>> {
		const response = await this.executor.dispatch(query, variables);

		return <APIResponse<T>>this.finalizeResponse(response);
	}

	public async createPost(
		title: string,
		content: string
	): Promise<APIResponse<{ createPost: string }>> {
		if (!isAuthenticated) throw new Error("must be authenticated");
		return this.executeQuery(queries.createPost, { title, content });
	}

	public async userData(target?: string): Promise<
		APIResponse<{
			userData: {
				name: string;
				accountType: AccountType;
			};
		}>
	> {
		if (!isAuthenticated && target) throw new Error("must be authenticated");
		return this.executeQuery(queries.userData, target ? { target } : {});
	}

	public async getComments(gameName: string): Promise<
		APIResponse<{
			getGame: {
				comments: Array<{
					author: string;
					content: string;
					epoch: number;
					accountType: AccountType;
					id: string;
				}>;
			};
		}>
	> {
		return this.executeQuery(queries.getComments, { gameName });
	}

	public async createComment(
		gameName: string,
		content: string
	): Promise<
		APIResponse<{
			createComment: {
				epoch: number;
				author: string;
				content: string;
				accountType: AccountType;
				id: string;
			};
		}>
	> {
		return this.executeQuery(queries.createComment, { gameName, content });
	}

	public async likeGame(gameName: string): Promise<
		APIResponse<{
			likeGame: string;
		}>
	> {
		return this.executeQuery(queries.likeGame, { gameName });
	}

	public async unlikeGame(gameName: string): Promise<
		APIResponse<{
			unlikeGame: string;
		}>
	> {
		return this.executeQuery(queries.unlikeGame, { gameName });
	}

	public async createAccount(
		username: string,
		password: string
	): Promise<
		APIResponse<{
			createAccount: string;
		}>
	> {
		return this.executeQuery(queries.createAccount, { username, password });
	}

	public async login(
		username: string,
		password: string
	): Promise<
		APIResponse<{
			login: string;
		}>
	> {
		return this.executeQuery(queries.login, { username, password });
	}

	public async userReport(
		content: string,
		target: string
	): Promise<
		APIResponse<{
			userReport: string;
		}>
	> {
		return this.executeQuery(queries.userReport, { content, target });
	}

	public async deleteAccount(target: Optional<string> = null): Promise<
		APIResponse<{
			deleteAccount: string;
		}>
	> {
		return this.executeQuery(queries.deleteAccount, { target });
	}

	public async promoteAccount(target: string): Promise<
		APIResponse<{
			promoteAccount: string;
		}>
	> {
		return this.executeQuery(queries.promoteAccount, { target });
	}

	public async demoteAccount(target: string): Promise<
		APIResponse<{
			demoteAccount: string;
		}>
	> {
		return this.executeQuery(queries.demoteAccount, { target });
	}

	public async deleteGame(target: string): Promise<
		APIResponse<{
			deleteGame: string;
		}>
	> {
		return this.executeQuery(queries.deleteGame, { target });
	}

	public async apply(
		discordTag: string,
		questionOne: boolean,
		questionTwo: boolean,
		anythingElse: Optional<string> = null
	): Promise<
		APIResponse<{
			apply: string;
		}>
	> {
		return this.executeQuery(queries.apply, {
			discordTag,
			questionOne,
			questionTwo,
			anythingElse,
		});
	}

	public async deleteComment(
		gameName: string,
		commentId: string
	): Promise<
		APIResponse<{
			deleteComment: string;
		}>
	> {
		return this.executeQuery(queries.deleteComment, { gameName, commentId });
	}

	public async issueReport(
		gameName: string,
		content: string
	): Promise<
		APIResponse<{
			issueReport: string;
		}>
	> {
		console.log({ gameName, content });
		return this.executeQuery(queries.issueReport, { gameName, content });
	}
}
