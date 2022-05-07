import type { NextPage } from "next";
import Layout from "../components/layout";

const Home: NextPage = () => {
	return (
		<Layout title="test">
			<div className="text-white">
				<h1>hi</h1>
			</div>
		</Layout>
	);
};

export default Home;
