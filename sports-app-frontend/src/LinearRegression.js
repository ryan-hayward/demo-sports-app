import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
import * as d3 from 'd3';


function LinearRegression() {

	const [data, setData] = useState([]);

	// get data
	useEffect(() => {
		// hard code params inside useEffect for now
		const params = {
			x_var: 'home_pass_att',
			y_var: 'home_pass_yds'
		}
		axios({
			method: 'get',
			url: 'http://127.0.0.1:8000/analyzer/linreg/',
			params: params
		})
		.then(response => {
			setData(response.data)
		})
		.catch(error => {
			console.log(error);
			});
	}, [])

	const svgRef = useRef();
	if(data) {
		//container specs
		const width = 500; //configurable w and h
		const height = 300;
		const svg = d3.select(svgRef.current)
			.attr('width', width)
			.attr('height', height)
			.style('overflow', 'visible')
			.style('margin-top', '100px')
			.style('margin-left', '400px')
		//scaling
		const xScale = d3.scaleLinear()
			.domain([0, Math.ceil(data.x_max / 10) * 10]) // come back and change these with min and max x
			.range([0, width]); // consume the entire range of pixels
		const yScale = d3.scaleLinear()
			.domain([0, Math.ceil(data.y_max / 10) * 10]) // come back and changee these with min and max y
			.range([height, 0]) //d3 graphs start from top-left
		//axis setup
		const xAxis = d3.axisBottom(xScale).ticks(10) //arbitrary; number of ticks
		const yAxis = d3.axisLeft(yScale).ticks(10)
		svg.append('g')
			.call(xAxis)
			.attr('transform', 'translate(0, 300)'); //hardcoded height in for now
		svg.append('g')
			.call(yAxis)
		//axis labeling
		svg.append('text')
			.attr('x', width/2) // put x-axis label in middle of width
			.attr('y', height + 50) // put x-axis below graph
			.text(data.x_var); // TODO: add x label in here
		svg.append('text')
			.attr('y', height/2)
			.attr('x', -200)
			.text(data.y_var) // put y-axis labels here
		// draw dots on plot
		svg.selectAll()
			.data(data.td_array)
			.enter()
			.append('circle')
				.attr('cx', d => xScale(d[0]))
				.attr('cy', d => yScale(d[1]))
				.attr('r', 2) //arbitrary radius size
	}
  	//return html block
  	return (
        <div className="LinearRegression">
            <svg ref={svgRef}></svg>
        </div>
    );
}

export default LinearRegression;