import threading
import time
import datetime

def test_performance(
    concurrent_users=100, acceptable_response_time=0.01, elapsed_time=1, port=5000
):
    print()
    success_count = 0
    failure_count = 0
    global_threads = []
    threading_active_count = threading.active_count()

    def wait_for_threads_to_complete(threads, set_mfa_confirmed=False):

        all_finished = False
        while not all_finished:
            all_finished = True
            for thread in threads:
                alive = thread.is_alive()
                if alive:
                    all_finished = False
                    time.sleep(0.5)
                    # break back to the while
                    break
                pass
        return

    def access_pdf():
        # ping the route using requests
        return "test"

    # ======================================= Test Start =================================================

    case = f"Log in some users chosen at random with confirmed MFA as fast as we can "
    timing_array = []
    global_threads = []
    for __ in range(concurrent_users):

        threaded_function = get_random_retailer_user_and_log_on
        kwargs = dict(timing_array=timing_array,set_mfa_confirmed_true=True, set_mfa_confirmed_false=False )
        args = []
        thread = threading.Thread(target=threaded_function, args=args, kwargs=kwargs)
        global_threads.append(thread)
        thread.start()

        # handle the elapsed time
        sleep_time = elapsed_time / concurrent_users
        time.sleep(sleep_time)

    wait_for_threads_to_complete(global_threads)

    average_response_time = sum(timing_array) / len(timing_array)

    case = f"""
        {case}
        NB. A production level web server should be used for this test. Stop the debug server and use the 
        waitress server by running: run_waitress.bat
        {concurrent_users} individual retailer users be able to retrieve the league table over  {elapsed_time} second period
        with average response of each transaction faster than {acceptable_response_time} seconds. 
        The actual average was: {round(average_response_time, 3)} seconds.
     """

    if average_response_time <= acceptable_response_time:
        success_count = success_count + 1
        print(f"""[SUCCESS] Performance... """)
        print(f"""{case}""")
    else:
        failure_count = failure_count + 1
        print(f"[FAILURE] {case}")

    # ======================================= Test End ==================================================


    return success_count, failure_count

if __name__ == "__main__":

    port = 5000

    success_fail_counts = []

    success_fail_counts.append(
        test_performance(
            concurrent_users=20,
            elapsed_time=0.5,
            acceptable_response_time=0.5,
            port=port,
        )
    )  


    success_total = 0
    failure_total = 0
    for success_fail_count in success_fail_counts:
        success_count, fail_count = success_fail_count
        success_total = success_total + success_count
        failure_total = failure_total + fail_count

    print(
        f"""

        [NARRATIVE for FINAL RESULT]

        [FINAL RESULT] There were a total of {failure_total + success_total} api tests. {success_total} of them passed. {failure_total} of them failed"

        """
    )
