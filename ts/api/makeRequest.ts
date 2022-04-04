import { Buffer } from "buffer";

function makeHeader(values: Authorization) {
    const encoded = Buffer.from(
        `${values.username}:${values.password}`
    ).toString("base64");
    return `Basic ${encoded}`;
}

export default async <T>(
    query: string,
    variables: Optional<Variables> = null,
    auth: Optional<Authorization> = null
): Promise<T> => {
    console.log(query);
    const response = await fetch("/graphql", {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: auth ? makeHeader(auth) : "",
        },
        method: "POST",
        body: JSON.stringify({
            query,
            variables,
        }),
    });

    const json: GraphQLResponse<T> = await response.json();

    if (!response.ok) {
        throw new Error(`GraphQL request failed: ${json.errors!.message}`);
    }

    return json.data!;
};
