export default <T>(response: GraphQLResponse<T>): void => {
    const json = response.json;

    if (json.errors) {
        if (json.errors!.length > 1) {
            json.errors!.forEach(err => {
                console.error(`GraphQL request error: ${err.message}`);
            });

            throw new Error("GraphQL request failed");
        } else
            throw new Error(
                `GraphQL request failed: ${json.errors![0].message}`
            );
    }
};
