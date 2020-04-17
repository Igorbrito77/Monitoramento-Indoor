const knex = require('knex');
const fetch = require('node-fetch');

module.exports = {
    list
}

async function list(req, res){


    const url = `https://www.dcc.ufrrj.br/ocupationdb/api.php?period_from=2019-12-06%2008:00:00&period_to=2019-12-06%2011:00:00&type=data&mac_id=813`;
   

    const response = await fetch(
       url,
        {
            method: 'GET',
            
            headers:  {
                'Content-Type': 'application/json',
            }
        }
    );

    return  await response.json();
}
