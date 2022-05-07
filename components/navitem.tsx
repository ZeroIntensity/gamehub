import { ReactNode, FC } from "react";

type Props = { url: string; Svg: () => JSX.Element; title: string };

const NavItem: FC<Props> = ({ url, title, Svg }) => {
	return (
		<div>
			<a
				href={url}
				className="flex items-center space-x-3 text-white p-2 rounded-md font-medium hover:bg-zinc-700 focus:shadow-outline"
			>
				<span className="text-white m-auto md:m-0">
					<Svg />
				</span>
				<span className="hidden md:inline 2xl:text-xl">{title}</span>
			</a>
		</div>
	);
};

export default NavItem;
