const headers: GQLHeaders = {
    Accept: "application/json",
    "Content-Type": "application/json",
};

export default async <T extends object>(
    query: string,
    variables?: Variables,
    auth?: string
): Promise<GraphQLResponse<T>> => {
    if (auth) headers["Authorization"] = auth;

    const response = await fetch("/graphql", {
        headers,
        method: "POST",
        body: JSON.stringify({
            query,
            variables,
        }),
    });

    return await response.json();
};
