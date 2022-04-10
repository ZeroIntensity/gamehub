export const gql = (data: any): Query => new Query(data[0]);
// shitiest vscode extension goes to: graphql

export class Query {
    readonly raw: string;
    readonly scheme: GraphQLScheme;
    readonly name: string;
    readonly body: string;

    constructor(q: string) {
        let query: string = q;

        while (query[0] == " " || query[0] == "\n") {
            query = query.slice(1);
        }

        this.raw = query;

        const splitFirst = <GraphQLScheme>query.split(" ")[0];
        this.scheme = splitFirst;
        this.name = query.substring(splitFirst.length, query.indexOf("("));
        this.body = query.substring(query.indexOf("{"), query.length - 1);
    }
}
