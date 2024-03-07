import React, {useState, useEffect} from 'react';
import axios from 'axios';
import ScatterChart from "./ScatterChart";

function LinearRegression() {
	const [data, setData] = useState('');
  
  	useEffect((params = {
		x_var: 'home_pass_att',
		y_var: 'home_pass_yds'
	}) => {
    	axios({
      		method: 'get',
      		url: 'http://127.0.0.1:8000/analyzer/linreg/',
			params: params
    	})
		.then(response => {
        	console.log(response)
			// set two-dim array to be used in script below
			setData(response.data.td_array)
      	})
		.catch(error => {
        	console.log(error)
      	})
		//optional return function can be placed here
  	}, []) // the dependency array
	// return null if no data is provided by server
	if (!data) {
		return null
	}
  	//return html block
  	return (
        <div style={{height:'50%', width:'50%', marginTop:10, display:'inline-block'}}>
            <ScatterChart data={data} xVal={data[0]} yVal={data[1]}/>
        </div>
    )
}

export default LinearRegression;