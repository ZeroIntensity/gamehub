require("dotenv").config();

module.exports = {
	plugins: {
		tailwindcss: {},
		autoprefixer: {},
		"postcss-import": {},
		...(process.env.PRODUCTION ? { cssnano: {} } : {}),
	},
};
