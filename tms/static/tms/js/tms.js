
var dataView;
var draggableGrouping;
var grid;
var data = [];
var columns = [
    {id: "sel", name: "#", field: "sel", cssClass: "cell-selection", width: 40, resizable: false, selectable: false, focusable: false,
    grouping: {}
    },
    {id: "title", name: "Title", field: "title", width: 70, minWidth: 50, cssClass: "cell-title", sortable: true, editor: Slick.Editors.Text,
    grouping: {
        getter: "title",
        formatter: function (g) {
        return "Title:  " + g.value + "  <span style='color:green'>(" + g.count + " items)</span>";
        },
        aggregators: [
        new Slick.Data.Aggregators.Sum("cost")
        ],
        aggregateCollapsed: false,
        collapsed: false
    }
    },
    {id: "duration", name: "Duration", field: "duration", width: 70, sortable: true, groupTotalsFormatter: sumTotalsFormatter,
    grouping: {
        getter: "duration",
        formatter: function (g) {
        return "Duration:  " + g.value + "  <span style='color:green'>(" + g.count + " items)</span>";
        },
        aggregators: [
        new Slick.Data.Aggregators.Sum("cost")
        ],
        aggregateCollapsed: false,
        collapsed: false
    }
    },
    
    {id: "start", name: "Start", field: "start", minWidth: 60, sortable: true,
    grouping: {
        getter: "start",
        formatter: function (g) {
        return "Start:  " + g.value + "  <span style='color:green'>(" + g.count + " items)</span>";
        },
        aggregators: [
        new Slick.Data.Aggregators.Sum("cost")
        ],
        aggregateCollapsed: false,
        collapsed: false
    }
    },
    {id: "finish", name: "Finish", field: "finish", minWidth: 60, sortable: true,
    grouping: {
        getter: "finish",
        formatter: function (g) {
        return "Finish:  " + g.value + "  <span style='color:green'>(" + g.count + " items)</span>";
        },
        aggregators: [
        new Slick.Data.Aggregators.Sum("cost")
        ],
        aggregateCollapsed: false,
        collapsed: false
    }
    },
    {id: "cost", name: "Cost", field: "cost", width: 90, sortable: true, groupTotalsFormatter: sumTotalsFormatter,
    grouping: {
        getter: "cost",
        formatter: function (g) {
        return "Cost:  " + g.value + "  <span style='color:green'>(" + g.count + " items)</span>";
        },
        aggregators: [
        new Slick.Data.Aggregators.Sum("cost")
        ],
        aggregateCollapsed: false,
        collapsed: false
    }
    },
    {id: "effortDriven", name: "Effort Driven",  width: 80, minWidth: 20, maxWidth: 80, cssClass: "cell-effort-driven", field: "effortDriven", formatter: Slick.Formatters.Checkmark, sortable: true,
    grouping: {
        getter: "effortDriven",
        formatter :function (g) {
        return "Effort-Driven:  " + (g.value ? "True" : "False") + "  <span style='color:green'>(" + g.count + " items)</span>";
        },
        aggregators: [
        new Slick.Data.Aggregators.Sum("cost")
        ],
        collapsed: false
    }
    }
];

var sortcol = "title";
var sortdir = 1;
var percentCompleteThreshold = 0;
var prevPercentCompleteThreshold = 0;

function avgTotalsFormatter(totals, columnDef) {
    var val = totals.avg && totals.avg[columnDef.field];
    if (val != null) {
    return "avg: " + Math.round(val) + "%";
    }
    return "";
}

function sumTotalsFormatter(totals, columnDef) {
    var val = totals.sum && totals.sum[columnDef.field];
    if (val != null) {
    return "total: " + ((Math.round(parseFloat(val)*100)/100));
    }
    return "";
}

function myFilter(item, args) {
    return item["percentComplete"] >= args.percentComplete;
}

function percentCompleteSort(a, b) {
    return a["percentComplete"] - b["percentComplete"];
}

function comparer(a, b) {
    var x = a[sortcol], y = b[sortcol];
    return (x == y ? 0 : (x > y ? 1 : -1));
}

var draggableEnabled = true;

function groupByTitle() {
    draggableGrouping.setDroppedGroups('title');
    grid.invalidate();
    grid.render();  
}

function clearGroupings() {
    draggableGrouping.clearDroppedGroups();
}


function toggleDraggableGrouping() {
    clearGroupings();
    if ( draggableEnabled == true ) {
    grid.setPreHeaderPanelVisibility(false);
    draggableEnabled = false;
    } else {
    grid.setPreHeaderPanelVisibility(true);
    draggableEnabled = true;
    }
}

function toggleGrouping(expand) {
    if(expand) {
    dataView.expandAllGroups();
    $(".slick-group-toggle-all").removeClass('collapsed').addClass('expanded');
    } else {
    dataView.collapseAllGroups();
    $(".slick-group-toggle-all").removeClass('expanded').addClass('collapsed');
    }
}

function loadData(count) {
    var someDates = ["01/01/2009", "02/02/2009", "03/03/2009"];
    data = [];
    // prepare the data
    for (var i = 0; i < count; i++) {
    var d = (data[i] = {});

    d["id"] = "id_" + i;
    d["num"] = i;
    d["title"] = "Task " + i;
    d["duration"] = Math.round(Math.random() * 14);
    d["percentComplete"] = Math.round(Math.random() * 100);
    d["start"] = someDates[ Math.floor((Math.random()*2)) ];
    d["finish"] = someDates[ Math.floor((Math.random()*2)) ];
    d["cost"] = Math.round(Math.random() * 10000) / 100;
    d["effortDriven"] = (i % 5 == 0);
    }
    dataView.setItems(data);
}

$(".grid-header .ui-icon")
    .addClass("ui-state-default ui-corner-all")
    .mouseover(function (e) {
        $(e.target).addClass("ui-state-hover")
    })
    .mouseout(function (e) {
        $(e.target).removeClass("ui-state-hover")
    });

$(function () {
    draggableGrouping = new Slick.DraggableGrouping({iconImage :'../images/delete.png', groupIconImage: '../images/column-grouping.png', dropPlaceHolderText: 'Drop a column header here to group by the column :)'});
    // draggableGrouping = new Slick.DraggableGrouping({iconCssClass :'slick-groupby-remove-image', groupIconCssClass: 'slick-column-groupable-image', dropPlaceHolderText: 'Drop a column header here to group by the column :)'});  
    // draggableGrouping = new Slick.DraggableGrouping();
    var options = {
    enableCellNavigation: true,
    editable: true,
    enableColumnReorder: draggableGrouping.getSetupColumnReorder,
    createPreHeaderPanel: true,
    showPreHeaderPanel: true,
    preHeaderPanelHeight: 25
    };

    var groupItemMetadataProvider = new Slick.Data.GroupItemMetadataProvider();
    dataView = new Slick.Data.DataView({
    groupItemMetadataProvider: groupItemMetadataProvider,
    inlineFilters: true
    });
    
    grid = new Slick.Grid("#myGrid", dataView, columns, options);

    // register the group item metadata provider to add expand/collapse group handlers
    grid.registerPlugin(groupItemMetadataProvider);
    grid.registerPlugin(draggableGrouping);
    grid.setSelectionModel(new Slick.CellSelectionModel());

    var pager = new Slick.Controls.Pager(dataView, grid, $("#pager"));
    var columnpicker = new Slick.Controls.ColumnPicker(columns, grid, options);


    grid.onSort.subscribe(function (e, args) {
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;

    dataView.sort(comparer, args.sortAsc);

    });

    // wire up model events to drive the grid
    dataView.onRowCountChanged.subscribe(function (e, args) {
    grid.updateRowCount();
    grid.render();
    });

    dataView.onRowsChanged.subscribe(function (e, args) {
    grid.invalidateRows(args.rows);
    grid.render();
    });


    var h_runfilters = null;

    // wire up the slider to apply the filter to the model
    $("#pcSlider,#pcSlider2").slider({
    "range": "min",
    "slide": function (event, ui) {
        Slick.GlobalEditorLock.cancelCurrentEdit();

        if (percentCompleteThreshold != ui.value) {
        window.clearTimeout(h_runfilters);
        h_runfilters = window.setTimeout(filterAndUpdate, 10);
        percentCompleteThreshold = ui.value;
        }
    }
    });


    function filterAndUpdate() {
    var isNarrowing = percentCompleteThreshold > prevPercentCompleteThreshold;
    var isExpanding = percentCompleteThreshold < prevPercentCompleteThreshold;
    var renderedRange = grid.getRenderedRange();

    dataView.setFilterArgs({
        percentComplete: percentCompleteThreshold
    });
    dataView.setRefreshHints({
        ignoreDiffsBefore: renderedRange.top,
        ignoreDiffsAfter: renderedRange.bottom + 1,
        isFilterNarrowing: isNarrowing,
        isFilterExpanding: isExpanding
    });
    dataView.refresh();

    prevPercentCompleteThreshold = percentCompleteThreshold;
    }

    // initialize the model after all the events have been hooked up
    dataView.beginUpdate();
    dataView.setFilter(myFilter);
    dataView.setFilterArgs({
    percentComplete: percentCompleteThreshold
    });
    loadData(1000);
    dataView.endUpdate();

    $("#gridContainer").resizable();
})
