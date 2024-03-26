'use client'
import React from 'react'

interface BioProps{
	playerId: string;
}

const GetPlayerBio =  async ({playerId}: BioProps) => {
	//assumee playerId is always deeboSamuel
	//add in fetch Player Bio given playerid
	// const res = await fetch('http://127.0.0.1:8000/football_api/standard_search?' + new URLSearchParams({
    // 	search_type: 'Game',
    // 	week: '1',
    // 	season: '2023'
  	// }),
	// { cache: 'no-store' })
	//const bio: Bio[] = await res.json()
	console.log(playerId)
	const bio = {
		name : 'Deebo Samuel',
		position: 'WR',
		team: 'San Francisco 49ers',
		height: '6-0',
		weight: '215',
		dob: '1/15/96',
		college: 'South Carolina',
		draft: 'R2 2019 (36 OVR)'
	}

    return (
        <div className='card w-96 bg-base-100 shadow-xl'>
			<div className='card-body'></div>
				<h2 className='card-title'>{bio.name}</h2>
				<ul>
					<li>Position: {bio.position}</li>
					<li>Team: {bio.team}</li>
					<li>Height: {bio.height}</li>
					<li>Weight: {bio.weight}</li>
					<li>Date of Birth: {bio.dob}</li>
					<li>College: {bio.college}</li>
					<li>Draft: {bio.draft}</li>
				</ul>
    	</div>
  	)
}

export default GetPlayerBio
