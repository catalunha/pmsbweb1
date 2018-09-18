$('#selecao').on('change', function() {
    if ( this.value == '1')
    {
      $("#ativos").show();
      $("#n_ativos").hide();
    }
    else if (this.value == '2')
    {
      $("#ativos").hide();
      $("#n_ativos").show();
    }
  });