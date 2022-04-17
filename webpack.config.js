require("dotenv").config();

module.exports = {
	entry: {
		index: "./ts/index.ts",
		games: "./ts/games.ts",
		error: "./ts/error.ts",
		login: "./ts/login.ts",
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
	mode: process.env.PRODUCTION ? "production" : "development",
};
