// Prepare sizes and scales
var x = d3.scale.ordinal().rangeBands([0, width]),
    z = d3.scale.linear().domain([0, 4]).clamp(true),
    c = d3.scale.category10().domain(d3.range(10));

// Add the svg canvas
var svg = d3.select("#matrix").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Set tooltip to transparent
var tip = d3.select("#tooltip")
        .attr("class", "tooltip")
        .style("opacity", 0);

// Set legend with groups
d3.select("#legend-svg").attr("height", 18*(groups.length+1));
groups.forEach(function(group, i) {
    d3.select("#legend-svg").append("rect")
        .attr("y", i*20)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill-opacity", 1)
        .style("fill", function (d) {
                return (i == groups.length-1) ? null : c(i);
            });
    d3.select("#legend-svg").append("text")
        .attr("x", 25)
        .attr("y", i*20+15)
        .text(group);
});

// Define matrix data
var matrix = [],
    nodes = root.modules,
    n = nodes.length;

// Compute index per node
nodes.forEach(function(node, i) {
    //node.index = i;
    node.index = node.order.group;
    node.count = 0;
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
});

// Convert links to matrix; count cardinals
root.dependencies.forEach(function(link) {
    matrix[link.source_index][link.target_index].z = link.cardinal;
    matrix[link.source_index][link.target_index].imports = JSON.stringify(link.imports);
    matrix[link.source_index][link.target_index].source_name = link.source_name;
    matrix[link.source_index][link.target_index].target_name = link.target_name;
    nodes[link.source_index].count += link.cardinal;
});

// Precompute the orders
var orders = {
    name: d3.range(n).sort(function(a, b) { return nodes[a].order.name.False - nodes[b].order.name.False; }),
    import: d3.range(n).sort(function(a, b) { return nodes[a].order.import.False - nodes[b].order.import.False; }),
    export: d3.range(n).sort(function(a, b) { return nodes[a].order.export.False - nodes[b].order.export.False; }),
    group: d3.range(n).sort(function(a, b) { return nodes[a].order.group.False - nodes[b].order.group.False; }),
    // FIXME: commented out until similarity order is ready
    //similarity: d3.range(n).sort(function(a, b) { return nodes[a].order.similarity.False - nodes[b].order.similarity.False; }),
    name_reverse: d3.range(n).sort(function(a, b) { return nodes[a].order.name.True - nodes[b].order.name.True; }),
    import_reverse: d3.range(n).sort(function(a, b) { return nodes[a].order.import.True - nodes[b].order.import.True; }),
    export_reverse: d3.range(n).sort(function(a, b) { return nodes[a].order.export.True - nodes[b].order.export.True; }),
    group_reverse: d3.range(n).sort(function(a, b) { return nodes[a].order.group.True - nodes[b].order.group.True; }),
    // FIXME: commented out until similarity order is ready
    //similarity_reverse: d3.range(n).sort(function(a, b) { return nodes[a].order.similarity.True - nodes[b].order.similarity.True; })
};

// The default sort order
x.domain(orders.group);

// Append draw area
svg.append("rect")
    .attr("class", "background")
    .attr("width", width)
    .attr("height", height);

// Add all rows
var row = svg.selectAll(".row")
    .data(matrix)
    .enter().append("g")
    .attr("class", "row")
    .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
    .each(row);

row.append("line").attr("x2", width);

row.append("text")
    .attr("x", -6)
    .attr("y", x.rangeBand() / 2)
    .attr("dy", ".32em")
    .attr("text-anchor", "end")
    .text(function(d, i) { return nodes[i].name; });

// Add all columns
var column = svg.selectAll(".column")
    .data(matrix)
    .enter().append("g")
    .attr("class", "column")
    .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

column.append("line").attr("x1", -width);

column.append("text")
    .attr("x", 6)
    .attr("y", x.rangeBand() / 2)
    .attr("dy", ".32em")
    .attr("text-anchor", "start")
    .text(function(d, i) { return nodes[i].name; });

// Add all cells
function row(row) {
    var cell = d3.select(this).selectAll(".cell");
    cell.data(row.filter(function(d) { return d.z; }))
        .enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return z(d.z); })
        .style("fill", function(d) { return nodes[d.x].group.index == nodes[d.y].group.index ? c(nodes[d.x].group.index) : null; })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);
}

function mouseover(p) {
    // Display tooltip
    tip.transition().duration(200).style("opacity", .9);
    tip.html(p.source_name + ' depends on ' +
        p.target_name + '<br>' + 'Cardinal: '+ p.z);
    tip     .style("left", (d3.event.pageX - 20) + "px")
            .style("top", (d3.event.pageY + 20) + "px");
    // Colorize names
    d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
}

function mouseout() {
    // Uncolorize names
    d3.selectAll("text").classed("active", false);
    // Hide tooltip
    tip.transition().delay(100).duration(600)
        .style("opacity", 0)
        .style("pointer-events", 'none');
}

// Bind order button to order functions
d3.select("#order").on("change", function() {
    order(this.value);
});

// Order animation
function order(value) {
    x.domain(orders[value]);

    var t = svg.transition().duration(2500);

    t.selectAll(".row")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
        .selectAll(".cell")
        .delay(function(d) { return x(d.x) * 4; })
        .attr("x", function(d) { return x(d.x); });

    t.selectAll(".column")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
}