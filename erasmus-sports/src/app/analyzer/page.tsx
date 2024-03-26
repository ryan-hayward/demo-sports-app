// routing system in next js based on convention
import React from 'react'

interface Game {
	gameid: string;
	week: number;
	season: number;
	home_team_code: string;
	away_team_code: string;
}

const AnalysisPage = async () => {
	const res = await fetch('http://127.0.0.1:8000/football_api/standard_search?' + new URLSearchParams({
    	search_type: 'Game',
    	week: '1',
    	season: '2023'
  	}),
	{ cache: 'no-store' })

	const games: Game[] = await res.json()

  	return (
    	<>
			<h1>Games</h1>
			<p>{new Date().toLocaleTimeString()}</p>
			<table className='table table-border'>
				<thead>
					<tr>
						<th>Home Team</th>
						<th>Away Team</th>
					</tr>
				</thead>
				<tbody>
					{games.map(game => <tr key={game.gameid}>
						<td>{game.home_team_code}</td>
						<td>{game.away_team_code}</td></tr>)}
				</tbody>
			</table>
		</>
  	)
}

export default AnalysisPage
