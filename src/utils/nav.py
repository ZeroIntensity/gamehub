import aiofiles
from typing import Optional
from ..db import FoundUser
from dataclasses import dataclass

__all__ = (
    "nav",
)

@dataclass
class NavItem:
    svg: str
    href: str
    title: str
    marker: bool = False

SVG_LOGOUT = """<svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                        />
                    </svg>"""
SVG_LOGIN = """<svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                        />
                    </svg>"""
SVG_HOME = """<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
						/>
					</svg>"""
SVG_GAMES = """<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"
						/>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z"
						/>
					</svg>"""
SVG_SUGGESTIONS = """<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
						/></svg
				>"""
SVG_APPLICATIONS = """<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
						/>
					</svg>"""
SVG_REPORT = """<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
						/>
					</svg>"""
SVG_SOURCE = """<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
						/>
					</svg>"""
SVG_PROFILE = """<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-7 w-7 md:h-6 md:w-6 2xl:w-8 2xl:h-8"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
					/>
				</svg>"""

NAVITEMS = [
    NavItem(SVG_HOME, '/', 'Home'),
    NavItem(SVG_GAMES, '/games', 'Games'),
    NavItem(SVG_SUGGESTIONS, '/suggestions', 'Suggestions'),
    NavItem(SVG_APPLICATIONS, '/applications', 'Application'),
    NavItem(SVG_REPORT, '/report', 'Report'),
]

def nav(user: Optional[FoundUser]):
	base: list =  [
        *NAVITEMS,
        NavItem('', '', '', True),
        NavItem(SVG_LOGIN, '/login', 'Login') if not user else \
            NavItem(SVG_LOGOUT, '/logout', 'Logout'),
        NavItem(SVG_SOURCE, 'https://github.com/ZeroIntensity/gamehub', 'Source'),
    ]

	if user:
		base.append(NavItem(SVG_PROFILE, '/profile/me', 'Profile'))

	return base
