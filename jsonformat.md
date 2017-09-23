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
				"parameter": "BDYMDL"
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
The parameters required for transforming data required for x_axis. There can be two values specified for the x-axis. One as a primary x-axis paramter, and the second as the categorical value for x-axis. Binning methods need to be specified  for the each of the axis parameters.

  *Applies to*: **bar**, **line**
  
  *Allowed Values*: **nested object**

* ### *primary* - [parent object - 'x-axis']
Object specifiying details on the primary x-axis paramters.

  *Applies to*: **inherit**
  
  *Allowed Values*: **nested object**
  
* ### *parameter* - [parent object - 'x-axis.primary']
The parameter name which has to be used for providing the data to the primary x-axis parameter. This should be the exact name of the database column.

  *Applies to*: **inherit**
  
  *Allowed Values*: 
  - REPAIR-DT
  - PAID-DT
  - Vehicle BUILT-DT
  - ENG BUILT-DT
  - TRN BUILT-DT
  - MLG
  
* ### *binning_method* - [parent object - 'x-axis.primary']
The [binning](https://en.wikipedia.org/wiki/Data_binning) method that has to be applied to group the values.

  *Applies to*: **inherit**
  
  *Allowed Values*:
  - number
  - date
  
  * ### *categorical* - [parent object - 'x-axis']
Object specifiying details on the primary x-axis paramters.

  *Applies to*: **inherit**
  
  *Allowed Values*: **nested object**
  
  
* ### *parameter* - [parent object - 'x-axis.categorical']
The parameter name which has to be used for providing the data to the categorical x-axis parameter. This should be the exact name of the database column.

  *Applies to*: **inherit**
  
  *Allowed Values*: 
  - RPR-DLR
  - CLAIM
  - BDY MDL
  - PART NO
  - VIN
  - ENG
  - TRAN
  
