from django.shortcuts import render,get_object_or_404, redirect
from .models import SnapshotSchedule
from .script import get_vm_uuidsc,get_pe,get_vms_form_pe
# Create your views here.
import json
from datetime import datetime, timedelta
from .tasks import take_snapshot
from celery import shared_task
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from .email import send_email
from django.utils.dateformat import format
import pytz



selected_items = []
creds = []
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request,'home.html')

def snapshot_schedule_list(request):
    schedules = SnapshotSchedule.objects.filter(snapshot_taken=False,snapshot_failed=False)
    return render(request, 'snapshot_schedule_list.html', {'schedules': schedules})

def past_snapshots(request):
    schedules = SnapshotSchedule.objects.filter(snapshot_taken=True)
    return render(request, 'past_snapshots.html', {'schedules': schedules})

def delete_snapshot_schedule(request, schedule_id):
    schedule = get_object_or_404(SnapshotSchedule, pk=schedule_id)
    schedule.delete()
    return redirect('snapshot_schedule_list')


def delete_past_schedule(request, schedule_id):
    schedule = get_object_or_404(SnapshotSchedule, pk=schedule_id)
    schedule.delete()
    return redirect('past_snapshots')

def pe_creds(request):
    j_file = "pe_list_generated.json"
    with open(j_file, 'r') as file:
        data = json.load(file)
    return render(request, 'pe.html', {'data': data})

def process_form(request):
    if request.method == 'POST':
        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')
        field3 = request.POST.get('field3')
        creds = [field1.strip(), field2.strip(), field3.strip()]
        #print(creds)
        res = get_pe(creds=creds)
        if res is None:
            print("PLEASE ENTER CORRECT PC CREDENTIALS")
            return render(request, 'error_page.html')  # Render the error page
        # Process the successful form submission
        return redirect('pe_creds')  # Redirect to the 'pe_creds' URL
    return render(request, 'index.html')  # Render the form page for GET requ


def process_pe(request):
    if request.method == 'POST':
        selected_pes = request.POST.getlist('selected_items')
        vms=[]
        for selected_pe in selected_pes:
            uuid, ip, name = selected_pe.split('|')
            # Process the data here as needed
            #print("UUID:", uuid)
            #print("IP:", ip)
            res = get_vms_form_pe(uuid=uuid, ip=ip,name=name)
            if res is None:
                return render(request, 'error_page.html')  # Render the error page
            vms = vms + res
        #print(vms)
        ind = 1
        for obj in vms:
            obj["index"]= ind
            ind=ind+1
        with open("vms_from_pe.json", "w") as json_file:
            json.dump(vms, json_file, indent=4)
        
        return redirect('display_vms')
    else:
        return render(request, 'error_page.html')


def display_vms(request):
    with open("vms_from_pe.json", 'r') as file:
        data = json.load(file)
    #print(data)
    return render(request,'display_vms.html',{'data':data})


def submit_vms(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        selected_vms = []
        for selected_item in selected_items:
            uuid, cip, cluster_name, name = selected_item.split('|')
            selected_vms.append({
                'uuid': uuid,
                'cip': cip,
                'cluster_name': cluster_name,
                'name': name,
            })
        
        return render(request, 'selected_vms.html', {'selected_vms': selected_vms})
    else:
        return render(request, 'error_page.html')
    

def save_ss(request):
    if request.method == 'POST':
        selected_vms = request.POST.getlist('selected_vms')
        for vm_data in selected_vms:
            vm_name, vm_uuid, cluster_name, cluster_ip = vm_data.split('|')
            snapshot_date = request.POST.get(f'snapshot_date_{selected_vms.index(vm_data) + 1}')
            snapshot_time = request.POST.get(f'snapshot_time_{selected_vms.index(vm_data) + 1}')
            snapshot_schedule = SnapshotSchedule.objects.create(
                vm_name=vm_name,
                vm_uuid=vm_uuid,
                snapshot_time=snapshot_time,
                snapshot_date=snapshot_date,
                cluster_ip=cluster_ip,
                cluster_name=cluster_name
            )
            # You can perform additional operations with the saved snapshot_schedule object if needed
        return redirect('snapshot_schedule_list')  # Redirect to a success page after saving
    else:
        return redirect('error_page')  # Redirect to an error page if the request method is not POST

  # Redirect to an error page if the request method is not POST

def save_ss(request):
    if request.method == 'POST':
        selected_vms = request.POST.getlist('selected_vms')
        for vm_data in selected_vms:
            vm_name, vm_uuid, cluster_name, cluster_ip = vm_data.split('|')
            snapshot_date = request.POST.get(f'snapshot_date_{selected_vms.index(vm_data) + 1}')
            snapshot_time = request.POST.get(f'snapshot_time_{selected_vms.index(vm_data) + 1}')
            snapshot_name = request.POST.get(f'snapshot_name_{selected_vms.index(vm_data) + 1}')

            print(snapshot_date,snapshot_time)
            snapshot_schedule = SnapshotSchedule.objects.create(
                vm_name=vm_name,
                vm_uuid=vm_uuid,
                snapshot_time=snapshot_time,
                snapshot_date=snapshot_date,
                cluster_ip=cluster_ip,
                cluster_name=cluster_name,
                task_id = None,
                snapshot_name = snapshot_name
            )
            # Store the task ID associated with the scheduled task
            #snapshot_schedule.task_id = schedule_snapshot_task(snapshot_schedule)
            snapshot_schedule.save()
        return redirect('snapshot_schedule_list')  # Redirect to a success page after saving
    else:
        return redirect('error_page')  # Redirect to


def format_datetime(dt):
    # Convert the datetime object to a human-friendly format
    dt = timezone.localtime(dt, timezone=timezone.get_current_timezone()) 
    formatted_date = dt.strftime("%d %b %Y")  # Format date as 'day month year'
    formatted_time = dt.strftime("%I:%M %p")  # Format time as 'hour:minute AM/PM'
    
    # Combine formatted date and time
    formatted_datetime = f"{formatted_date}, {formatted_time}"
    return formatted_datetime


def failed_snapshots(request):
    schedules = SnapshotSchedule.objects.filter(snapshot_taken=False, snapshot_failed=True)
    return render(request, 'failed_snapshots.html', {'schedules': schedules}) 


#@shared_task(bind=True)
#def check_ss(self):
def check_ss():
    """
    Task to check and execute snapshot schedules.

    This task checks the database for snapshot schedules that are due,
    executes the snapshot if the schedule time has passed, and sends
    email notifications regarding the success or failure of the snapshot.
    """
    print("Checking for snapshot schedules")

    # Get current date and time
    current_datetime = timezone.now()

    # Retrieve all SnapshotSchedule objects where snapshot is not taken
    snapshot_schedules = SnapshotSchedule.objects.filter(snapshot_taken=False, snapshot_failed=False)

    # Convert queryset to list of dictionaries
    snapshot_schedules_data = list(snapshot_schedules.values())

    # Serialize the data to JSON and write to a file
    with open("current_snapshot_schedules.json", "w") as json_file:
        json.dump(snapshot_schedules_data, json_file, cls=DjangoJSONEncoder, indent=4)

    # Check if there are no snapshot schedules
    if not snapshot_schedules:
        print("No snapshot schedules found")
        return None

    ist = pytz.timezone('Asia/Kolkata')
    # Iterate over each SnapshotSchedule object
    for snapshot_schedule in snapshot_schedules:
        # Combine date and time fields to create a datetime object
        snapshot_datetime = timezone.make_aware(
            timezone.datetime.combine(snapshot_schedule.snapshot_date, snapshot_schedule.snapshot_time)
        )

        # Check if the scheduled datetime has passed
        if snapshot_datetime <= current_datetime:
            print("Time matched.")
            print("Current datetime:", current_datetime)
            print("Snapshot scheduled datetime:", snapshot_datetime)

            # Call the take_snapshot function for this SnapshotSchedule
            print("Attempting to Take Snapshot ")
            res = take_snapshot(snapshot_schedule.vm_uuid, snapshot_schedule.cluster_ip, snapshot_schedule.snapshot_name)

            if res is None:

                # If snapshot failed, reschedule for one hour later
               # new_snapshot_datetime = snapshot_datetime + timedelta(hours=1)
               # snapshot_schedule.snapshot_date = new_snapshot_datetime.date()
               # snapshot_schedule.snapshot_time = new_snapshot_datetime.time()
                snapshot_schedule.snapshot_failed = True
                snapshot_schedule.save()

                # Send failure email notification
                send_email(snapshot_schedule.vm_name, snapshot_schedule.cluster_name, snapshot_schedule.snapshot_name, message_info="failed")
                print("Snapshot failed")
            else:
                # If snapshot succeeded, update the schedule
                snapshot_schedule.snapshot_taken = True

                now_ist = timezone.now().astimezone(ist)
                snapshot_schedule.snapshot_execution_datetime = format(now_ist, 'd M Y, h:i A')
                snapshot_schedule.save()

                # Send success email notification
                send_email(snapshot_schedule.vm_name, snapshot_schedule.cluster_name, snapshot_schedule.snapshot_name, message_info="success")
                print("Snapshot success")
        else:
            print("Time not matched.")
            print(current_datetime, snapshot_datetime)