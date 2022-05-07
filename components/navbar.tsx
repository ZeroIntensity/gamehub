import Home from "../public/svg/home.svg";
import Games from "../public/svg/games.svg";
import Suggestions from "../public/svg/suggestions.svg";
import Applications from "../public/svg/applications.svg";
import Report from "../public/svg/report.svg";
import Login from "../public/svg/login.svg";
import Logout from "../public/svg/logout.svg";
import Source from "../public/svg/source.svg";
import Profile from "../public/svg/profile.svg";
import NavItem from "./navitem";

const SVG_PROPS = {
	className: "h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8",
};

const Navbar = () => {
	return (
		<nav className="w-3/12 bg-zinc-800 rounded p-3 shadow-lg self-start sticky top-0 h-screen overflow-y-auto">
			<div className="flex space-x-4 p-2 mb-5 justify-center">
				<p className="text-white text-2xl lg:text-5xl font-bold tracking-wide">
					Game
					<span className="bg-gradient-to-r from-orange-400 to-orange-500 bg-clip-text text-transparent">
						Hub
					</span>
				</p>

				<p></p>
			</div>

			<svg className="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"></svg>

			<div className="space-y-2">
				{[
					{
						title: "Home",
						url: "/",
						Svg: () => <Home {...SVG_PROPS} />,
					},
					{
						title: "Games",
						url: "/games",
						Svg: () => <Games {...SVG_PROPS} />,
					},
					{
						title: "Suggestions",
						url: "/suggestions",
						Svg: () => <Suggestions {...SVG_PROPS} />,
					},
					{
						title: "Applications",
						url: "/applications",
						Svg: () => <Applications {...SVG_PROPS} />,
					},
					{
						title: "Reports",
						url: "/reports",
						Svg: () => <Report {...SVG_PROPS} />,
					},
				].map(({ title, url, Svg }) => (
					<NavItem title={title} url={url} Svg={Svg} />
				))}
				<div className="py-4">
					<hr className="w-full border-t border-zinc-700" />
				</div>

				{[
					{
						title: "Source",
						url: "/",
						Svg: () => <Source {...SVG_PROPS} />,
					},
				].map(({ title, url, Svg }) => (
					<NavItem title={title} url={url} Svg={Svg} />
				))}
			</div>
		</nav>
	);
};

export default Navbar;
