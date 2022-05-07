import React, { ReactNode } from "react";
import Head from "next/head";
import Navbar from "./navbar";

type Props = {
	children: ReactNode;
	title: string;
};

const Layout: React.FC<Props> = ({ children, title }) => {
	return (
		<>
			<Head>
				<title>{title} - GameHub</title>
			</Head>

			<main className="bg-zinc-900">
				<div className="flex flex-wrap bg-zinc-900 w-full h-screen">
					<Navbar />
					<div className="w-9/12 text-white">{children}</div>
				</div>
			</main>
		</>
	);
};

export default Layout;
