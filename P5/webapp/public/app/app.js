(function() {
    var Ploter = {
        init: function() {
            this.DATAURL = 'http://localhost:3030/api/v1/eurostat/basic/country/';
            this.DURATION = 1500;
            this.DELAY    = 500;

            this.data = []
            // bind all events
            this.bindEvents();            
        },

        getPieDataForYear: function( year ) {
            var pieData = [];
            var total = 0.;
            // retreive the data for the year of choice
            for (var idx in this.data.pieChart) {            
                if (this.data.pieChart[idx].year == year) {
                    pieData.push(this.data.pieChart[idx])
                    total += this.data.pieChart[idx].value
                }
            }
            // convert the value into pct
            for (var idx in pieData) {
                val = pieData[idx].value;
                pieData[idx].value =  val / total
            }
            return pieData;
        },

        drawPieChart: function( elementId, date ) {

            year = date.getFullYear()
            document.getElementById("title").innerHTML = "Eurning Structure for " + year;
            var data = this.getPieDataForYear(year)

            var containerEl = document.getElementById( elementId ),        
            width       = containerEl.clientWidth,
            height      = width * 0.4,
            radius      = Math.min( width, height ) / 2,
            container   = d3.select( containerEl ),
            svg         = container.select( 'svg' )
                                  .attr( 'width', width )
                                  .attr( 'height', height + 30 );        
            var pie = svg.append( 'g' )
                .attr(
                    'transform',
                    'translate(' + width / 2 + ',' + height / 2 + ')'
                );
        
            var detailedInfo = svg.append( 'g' )
                .attr( 'class', 'pieChart--detailedInformation' );

            var twoPi   = 2 * Math.PI;
            var pieData = d3.layout.pie()
                .value( function( d ) { return d.value; } ).sort(null);

            var arc = d3.svg.arc()
                .outerRadius( radius - 20)
                .innerRadius( 0 );

            // remove data not being used
            pie.datum(data).selectAll("path")
                .data(pieData).exit().remove();
            svg.selectAll('text').remove();
            svg.selectAll('line').remove();
            svg.selectAll('.pieChart--detail--textContainer').remove();

            // add any new paths
            var self = this;
            var pieChartPieces = pie.datum( data )
                .selectAll( 'path' )
                .data( pieData )
                .enter()
                .append( 'path' )
                .attr( 'class', function( d ) {
                    return 'pieChart__' + d.data.color;
                } )
                .attr( 'filter', 'url(#pieChartInsetShadow)' )
                .attr( 'd', arc )
                .each( function() {
                    self._current = { startAngle: 0, endAngle: 0 }; 
                } )
                .transition()
                .duration( this.DURATION )
                // Store the displayed angles in _current.
                // Then, interpolate from _current to the new angles.
                // During the transition, _current is updated in-place by d3.iterpolate.
                .attrTween( 'd', function( d ) {
                    var interpolate = d3.interpolate( self._current, d );
                    self._current = interpolate( 0 );
        
                    return function( t ) {
                        return arc( interpolate( t ) );
                    };
                } )
                .each( 'end', function handleAnimationEnd( d ) {
                    drawDetailedInformation( d.data, this ); 
                } );

            drawChartCenter(); 
            
            function drawChartCenter() {
                var centerContainer = pie.append( 'g' )
                                        .attr( 'class', 'pieChart--center' );
              
                centerContainer.append( 'circle' )
                              .attr( 'class', 'pieChart--center--outerCircle' )
                              .attr( 'r', 0 )
                              .attr( 'filter', 'url(#pieChartDropShadow)' )
                              .transition()
                              .duration( self.DURATION )
                              .delay( self.DELAY )
                              .attr( 'r', radius - 50 );
              
                centerContainer.append( 'circle' )
                              .attr( 'id', 'pieChart-clippy' )
                              .attr( 'class', 'pieChart--center--innerCircle' )
                              .attr( 'r', 0 )
                              .transition()
                              .delay( self.DELAY )
                              .duration( self.DURATION )
                              .attr( 'r', radius - 55 )
                              .attr( 'fill', '#fff' );
            }
        
            function drawDetailedInformation ( data, element ) {
                var bBox      = element.getBBox(),
                    infoWidth = width * 0.3,
                    anchor,
                    infoContainer,
                    position;            

                if ( ( bBox.x + bBox.width / 2 ) > 0 ) {                    
                    infoContainer = detailedInfo.append( 'g' )
                                            .attr( 'width', infoWidth )
                                            .attr(
                                              'transform',
                                              'translate(' + ( width - infoWidth ) + ',' + ( bBox.height + bBox.y ) + ')'
                                            );
                    anchor   = 'end';
                    position = 'right';
                } else {
                    infoContainer = detailedInfo.append( 'g' )
                                                .attr( 'width', infoWidth )
                                                .attr(
                                                  'transform',
                                                  'translate(' + 0 + ',' + ( bBox.height + bBox.y + 50 ) + ')'
                                                );
                    anchor   = 'start';
                    position = 'left';
                }

                infoContainer.data( [ data.value * 100 ] )
                    .append( 'text' )
                    .text ( '0 %' )
                    .attr( 'class', 'pieChart--detail--percentage' )
                    .attr( 'x', ( position === 'left' ? 0 : infoWidth ) )
                    .attr( 'y', -10 )
                    .attr( 'text-anchor', anchor )
                    .transition()
                    .duration( self.DURATION )
                    .tween( 'text', function( d ) {
                        var i = d3.interpolateRound(
                            +this.textContent.replace( /\s%/ig, '' ),
                            d
                        );

                        return function( t ) {
                            this.textContent = i( t ) + ' %';
                        };
                    });
              
                infoContainer.append( 'line' )
                            .attr( 'class', 'pieChart--detail--divider' )
                            .attr( 'x1', 0 )
                            .attr( 'x2', 0 )
                            .attr( 'y1', 0 )
                            .attr( 'y2', 0 )
                            .transition()
                            .duration( self.DURATION )
                            .attr( 'x2', infoWidth );
              
                infoContainer.data( [ data.description ] ) 
                            .append( 'foreignObject' )
                            .attr( 'width', infoWidth ) 
                            .attr( 'height', 100 )
                            .append( 'xhtml:body' )
                            .attr(
                                'class',
                                'pieChart--detail--textContainer ' + 'pieChart--detail__' + position
                            )
                            .html( data.description );
            }
        },
        
        drawLineChart: function( elementId, data ) {
            var self = this;
            // draw one line per code
            var dataGroup = d3.nest()
                .key(function(d) {
                        return d.code;
                    })
                .entries(data);
            
            var parseDate = d3.time.format("%Y").parse;
             
            var containerEl = document.getElementById( elementId ),
                width       = containerEl.clientWidth,
                height      = width * 0.4,
                margin      = {
                  top    : 30,
                  right  : 10,
                  left   : 10 
                },
                
                detailWidth  = 98,
                detailHeight = 55,
                detailMargin = 10,

                container   = d3.select( containerEl ),
                svg         = container.select( 'svg' )
                                    .attr( 'width', width )
                                    .attr( 'height', height + margin.top ),

                x          = d3.time.scale().range( [ 0, width - detailWidth ] ),

                xAxis      = d3.svg.axis().scale( x )
                                          .ticks ( 8 )
                                          .tickSize( -height ),
                xAxisTicks = d3.svg.axis().scale( x )
                                          .ticks( 16 )
                                          .tickSize( -height )
                                          .tickFormat( '' ),
                y          = d3.scale.linear().range( [ height, 0 ] ),
                yAxisTicks = d3.svg.axis().scale( y )
                                          .ticks( 12 )
                                          .tickSize( width )
                                          .tickFormat( '' )
                                          .orient( 'right' ),
                area = d3.svg.area()
                          .interpolate( 'linear' )
                          .x( function( d )  { return x( d.year ) + detailWidth / 2; } )
                          .y0( height )
                          .y1( function( d ) { return y( d.value ); } ),

                line = d3.svg.line()
                          .interpolate( 'linear' )
                          .x( function( d ) { return x( d.year ) + detailWidth / 2; } )
                          .y( function( d ) { return y( d.value ); } ),

                startData = dataGroup.map( function( d ) {
                    return {
                        year : d.year,
                        value : d.value
                    }
                }),

                circleContainer;

            // remove data not being used
            svg.selectAll('path').remove();
            svg.selectAll('circle').remove();
            svg.selectAll('g').remove();

            // Compute the minimum and maximum date, and the maximum value.
            x.domain( [ data[ 0 ].year, data[ data.length - 1 ].year ] );
            y.domain( [ 0, d3.max( data, function( d ) { return d.value + 15000; } ) ] );

            svg.append( 'g' )
                .attr( 'class', 'lineChart--xAxisTicks' )
                .attr( 'transform', 'translate(' + detailWidth / 2 + ',' + height + ')' )
                .call( xAxisTicks );

            svg.append( 'g' )
                .attr( 'class', 'lineChart--xAxis' )
                .attr( 'transform', 'translate(' + detailWidth / 2 + ',' + ( height + 7 ) + ')' )
                .call( xAxis );

            svg.append( 'g' )
                .attr( 'class', 'lineChart--yAxisTicks' )
                .call( yAxisTicks );                        

            // Add the line path
            dataGroup.forEach(function(d, i) {
                svg.append('path')
                    .data( startData )
                    .attr( 'class', 'lineChart--areaLine--'+d.key )
                    .attr( 'd', line )
                    .transition()
                    .duration( self.DURATION )
                    .delay( self.DURATION / 2 )
                    .attrTween( 'd', tween( d.values, line ) )               
                    .attr('stroke-width', 2)
                    .attr('fill', 'none')
                    .each( 'end', function() {
                        drawCircles( data );
                    })
            });

            // Add the area path.
            dataGroup.forEach(function(d, i) {
                svg.append( 'path' )
                    .data( startData )
                    .attr( 'class', 'lineChart--area--'+d.key )
                    .attr( 'd', area )
                    .transition()
                    .duration( this.DURATION )
                    .attrTween( 'd', tween( d.values, area ) );
            });

            // Helper functions!!!
            function drawCircle( datum, index ) {

                circleContainer.datum( datum )
                    .append( 'circle' )
                    .attr( 'class', 'lineChart--circle--'+datum.code )
                    .attr( 'r', 0 )
                    .attr(
                        'cx',
                        function( d ) {
                            return x( d.year ) + detailWidth / 2;
                        }
                    )
                    .attr(
                        'cy',
                        function( d ) {
                            return y( d.value );
                        }
                    )
                    .on( 'mouseenter', function( d ) {
                        d3.select( this )
                            .attr(
                                'class',
                                'lineChart--circle--'+datum.code+' lineChart--circle--'+datum.code+'__highlighted' 
                            )
                        .attr( 'r', 7 );
                        d.active = true;
                        showCircleDetail( d );
                    } )
                    .on( 'mouseout', function( d ) {
                        d3.select( this )
                            .attr(
                                'class',
                                'lineChart--circle--'+datum.code
                            )
                        .attr( 'r', 6 );
                      
                    if ( d.active ) {
                        hideCircleDetails(); 
                        d.active = false;
                      }
                    } )
                    .on( 'click touch', function( d ) {
                        if ( d.active ) {
                            showCircleDetail( d )
                        } else {
                            hideCircleDetails();
                        }
                    } )
                    .transition()
                    .delay( self.DURATION / 10 * index )
                    .attr( 'r', 6 );
            }

            function drawCircles( data ) {
                circleContainer = svg.append( 'g' );

                data.forEach( function( datum, index ) {
                    drawCircle( datum, index );
                } );
            }
        
            function hideCircleDetails() {
                circleContainer.selectAll( '.lineChart--bubble' )
                    .remove();
            }
        
            function showCircleDetail( data ) {
                self.drawPieChart('pieChart', data.year)
                var details = circleContainer.append( 'g' )
                    .attr( 'class', 'lineChart--bubble' )
                    .attr(
                        'transform',
                        function() {
                            var result = 'translate(';
                            result += x( data.year );
                            result += ', ';
                            result += y( data.value ) - detailHeight - detailMargin;
                            result += ')';

                            return result;
                    }
                );
          
                details.append( 'path' )
                      .attr( 'd', 'M2.99990186,0 C1.34310181,0 0,1.34216977 0,2.99898218 L0,47.6680579 C0,49.32435 1.34136094,50.6670401 3.00074875,50.6670401 L44.4095996,50.6670401 C48.9775098,54.3898926 44.4672607,50.6057129 49,54.46875 C53.4190918,50.6962891 49.0050244,54.4362793 53.501875,50.6670401 L94.9943116,50.6670401 C96.6543075,50.6670401 98,49.3248703 98,47.6680579 L98,2.99898218 C98,1.34269006 96.651936,0 95.0000981,0 L2.99990186,0 Z M2.99990186,0' )
                      .attr( 'width', detailWidth )
                      .attr( 'height', detailHeight );
              
                var text = details.append( 'text' )
                        .attr( 'class', 'lineChart--bubble--text' );
              
                text.append( 'tspan' )
                  .attr( 'class', 'lineChart--bubble--label--' + data.code )
                  .attr( 'x', detailWidth / 2 )
                  .attr( 'y', detailHeight / 3 )
                  .attr( 'text-anchor', 'middle' )
                  .text( data.label );
              
                text.append( 'tspan' )
                  .attr( 'class', 'lineChart--bubble--value' )
                  .attr( 'x', detailWidth / 2 )
                  .attr( 'y', detailHeight / 4 * 3 )
                  .attr( 'text-anchor', 'middle' )
                  .text( data.value );
            }

            function tween( b, callback ) {
                return function( a ) {
                    var i = d3.interpolateArray( a, b );

                    return function( t ) {
                        return callback( i ( t ) );
                    };
                };
            }
        },

        parseData: function(json) {
            var self = this;
            // reset the data
            this.data = {
                lineChart: [],
                pieChart: []
            }
            json.map(function(d) {  
                var estruct = d.estruct;
                for (var idx in d.measure) {
                    // we are only interested about Tax and Net
                    if (['NET', 'TAX'].indexOf(estruct.code) >= 0) {
                        self.data.lineChart.push({
                            'code'      : estruct.code,
                            'label'     : estruct.description,
                            'year'      : new Date(d.measure[idx].year, 0),
                            'value'     : d.measure[idx].data
                        });

                        self.data.pieChart.push({
                            'color'           : ((estruct.code == 'NET') ? 'blue' : 'red'),
                            'description'     : ((estruct.code == 'NET') ?
                                'A compulsory contribution to state revenue, levied by the government on workers\' income and business profits.'
                                :
                                'Gross income minus taxes, allowances, and deductions. Value used to determine how much income tax is owed.'),
                            'title'           : estruct.description,
                            'value'           : d.measure[idx].data,
                            'year'            : d.measure[idx].year
                        })
                    }                
                }
            })
            return self.data;
        },        

        render: function(jsondata, country) {
            var self = this;

            document.getElementById("pie-title").innerHTML = country + " Eurnings (Single person without children)";
            document.getElementById("line-title").innerHTML = country + " Annual Earnings";

            // parse the json data coming from the middleware
            this.parseData(jsondata);
            
            // draw the line chart
            this.drawLineChart('lineChart', this.data.lineChart);
            // draw the pie chart
            date = new Date(2014, 0);
            this.drawPieChart('pieChart', date);                
        },

        bindEvents: function() {
            var self = this;
            var dropdown = d3.select("#countrySelector")
            var change = function() {
                var source = dropdown.node().options[dropdown.node().selectedIndex].value;
                var label = dropdown.node().options[dropdown.node().selectedIndex].label;
                d3.json(self.DATAURL + source)
                    .on("load", function(data) {self.render(data, label);})
                    .on("error", function(error) { console.log("failure!", error); })
                    .get();
               
            }
            dropdown.on("change", change);
            change()
        }
    }

    Ploter.init();

})();


