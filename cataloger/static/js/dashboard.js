$(document).ready(function() {
    $('#datasetTable').DataTable();
});

// set the table's sorting to column 1 (0 is a checkbox now)
$('#datasetTable').dataTable({
    "columnDefs": [
        { "orderable": false, "targets": 0 }
    ],
    "order": [[ 1, "asc"]]
});

// Check all checkboxes in this column
$('#selectAll').change(function() {
    if($(this).is(":checked")) {
        $(".checkboxSelection").each(function() {
            $(this).prop('checked', true);
        });
    }
    else {
        $(".checkboxSelection").each(function() {
            $(this).prop('checked', false);
        });
    }
});

// When all checkboxes are selected, check the "selectAll" box at the top
$(".checkboxSelection").change(function() {
    var allSelected = true;

    $(".checkboxSelection").each(function() {
        if(!$(this).is(":checked")) {
            $('#selectAll').prop('checked', false);
            allSelected = false;
        }
    });

    if(allSelected)
        $('#selectAll').prop('checked', true);
});

// Confirm deletion when deleting datasets
$('#datasetForm').submit(function() {
    var action = $('#datasetForm :input[name=action_type]');
    console.log("Action:" + action.val());
    if (action.val() == 'delete') {
        return confirm("Are you sure that you want to delete the selected items? This cannot be undone.");
    }
    else {
        return true;
    }
});
