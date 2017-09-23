## JSON Request Format Specification

Following is a concise description of the JSON Request format specifying the details of the Plot.

Example 1:
```javascript
{
	"plot_parameters":{
		"plot_type": "bar",
		"x_axis":{
			"primary" :{
				"parameter": "REPAIR-DT",
				"binning_method": "date"
			},
			"categorical":{
				"compare_parameter": "BDYMDL",
				"binning_method" : "numbers"
			}
		},
		"y_axis":{
			"aggregation_method": "SUM",
			"aggregation_parameter" : "AMOUNT(USD)"
		},
		"filters":[{
			"parameter":"RPRDLR",
			"operator": "=",
			"value": "098763",
			"type": "string"
		},{
			"parameter":"ENG",
			"operator": "=",
			"value": "SMP",
			"type" : "string"
		}
		]
	}
}
```

* ### *plot_type*
The Type of plot to be generated.

  *Applies to*: **all plot types**
  
  *Allowed Values*
  - bar
  - pie
  - line

* ### *x_axis*
The parameters required for transforming data required for x_axis

  *Applies to*: **bar**, **line**
  
  *Allowed Values*: **nested object**
