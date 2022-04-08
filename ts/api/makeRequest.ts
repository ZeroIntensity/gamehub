export default async <T>(
    query: string,
    variables?: Variables,
    auth?: string
): Promise<T> => {
    const response = await fetch("/graphql", {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify({
            query,
            variables,
        }),
    });

    const json: GraphQLResponse<T> = await response.json();

    if (json.errors) {
        throw new Error(
            `GraphQL request failed: ${json.errors!.forEach(message =>
                console.log(message)
            )}`
        );
    }

    return json.data!;
};
