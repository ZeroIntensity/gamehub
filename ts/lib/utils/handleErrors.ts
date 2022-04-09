export default <T>(response: GraphQLResponse<T>, normalError?: string) => {
    if (response.errors) {
        response.errors.forEach(err => {
            if (err.message != normalError) {
                console.error(`GraphQL request failed: ${err.message}`);
            }
        });
        return false;
    }
    return true;
};
