module.exports = {
    entry: {
        index: "./ts/index.ts",
    },
    module: {
        rules: [
            {
                use: "ts-loader",
                exclude: /node_modules/,
            },
        ],
    },
    output: {
        filename: "[name].js",
        path: __dirname + "/static/js/dist",
    },
    resolve: {
        extensions: [".ts", ".js"],
    },
};
