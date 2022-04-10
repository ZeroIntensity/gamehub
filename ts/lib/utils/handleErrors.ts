export default <T>(response: GraphQLResponse<T>): WrapperResponse => {
    const json = response.json;

    if ((response.status == 200 && json.errors) || json.errors?.length! > 1) {
        // for some reason an error returns 200 with strawberry
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

    if (json.errors) {
        return {
            ok: false,
            message: json.errors[0].message,
        };
    }

    return {
        ok: true,
    };
};
