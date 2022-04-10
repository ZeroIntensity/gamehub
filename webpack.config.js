module.exports = {
    entry: {
        index: "./ts/index.ts",
        games: "./ts/games.ts",
        error: "./ts/error.ts",
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
    target: "web",
    mode: "development",
};
