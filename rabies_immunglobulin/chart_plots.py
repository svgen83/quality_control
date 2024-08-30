from rabies_immunglobulin.models import (Batch, StandartSample,
                     SpecificationStandart,Document,
                     SpecificationParameter, Employee,
                     Method,                     
                     )

batches = Batch.objects.all().order_by('title')
a = []
for batch in batches:
    parameters = batch.batch_parameters.filter(
        title__title__contains="белка").values()
    a.append(parameters[0]['value'])
    
print(sum(a))

    for parameter in parameters:
        print(parameter['value'])
    print(a)
   
