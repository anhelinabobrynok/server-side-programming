import time
import pandas as pd
from multiprocessing import Pool, cpu_count, freeze_support
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .analytics_repositories import AnalyticsRepository


def process_genre_data(genre_id):
    time.sleep(0.01)  
    from .models import Genre
    try:
        genre = Genre.objects.get(genre_id=genre_id)
        return {
            'genre_id': genre_id,
            'name': genre.name,
            'processed': True
        }
    except:
        return None


def process_revenue_chunk(data_chunk):
    time.sleep(0.01)
    total = sum([float(item.get('total_revenue', 0) or 0) for item in data_chunk])
    return {'chunk_total': total, 'count': len(data_chunk)}


def sequential_processing(data_list, process_func):
    start_time = time.time()
    results = []
    for item in data_list:
        result = process_func(item)
        if result:
            results.append(result)
    end_time = time.time()
    return results, end_time - start_time


def parallel_processing_threads(data_list, process_func, max_workers=4):
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_func, item) for item in data_list]
        results = [f.result() for f in futures if f.result()]
    end_time = time.time()
    return results, end_time - start_time


def parallel_processing_processes(data_list, process_func, max_workers=None):
    if max_workers is None:
        max_workers = cpu_count()
    
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_func, item) for item in data_list]
        results = [f.result() for f in futures if f.result()]
    end_time = time.time()
    return results, end_time - start_time


@login_required
def parallel_performance_dashboard(request):
    
    try:
        genre_data = list(AnalyticsRepository.get_revenue_by_genre().values(
            'genre_id', 'name', 'total_revenue', 'total_tickets'
        ))
        
        if not genre_data:
            context = {
                'error': 'Немає даних для тестування'
            }
            return render(request, 'analytics/parallel_dashboard.html', context)
        
        genre_ids = [item['genre_id'] for item in genre_data]
        test_ids = genre_ids * 20  

        _, seq_time = sequential_processing(test_ids, process_genre_data)

        _, thread_time_2 = parallel_processing_threads(test_ids, process_genre_data, max_workers=2)
        _, thread_time_4 = parallel_processing_threads(test_ids, process_genre_data, max_workers=4)
        _, thread_time_8 = parallel_processing_threads(test_ids, process_genre_data, max_workers=8)

        cpu_cores = cpu_count()
        _, process_time_2 = parallel_processing_processes(test_ids, process_genre_data, max_workers=2)
        _, process_time_4 = parallel_processing_processes(test_ids, process_genre_data, max_workers=4)

        speedup_thread_2 = seq_time / thread_time_2 if thread_time_2 > 0 else 0
        speedup_thread_4 = seq_time / thread_time_4 if thread_time_4 > 0 else 0
        speedup_thread_8 = seq_time / thread_time_8 if thread_time_8 > 0 else 0
        speedup_process_2 = seq_time / process_time_2 if process_time_2 > 0 else 0
        speedup_process_4 = seq_time / process_time_4 if process_time_4 > 0 else 0
        
        chunks = [genre_data[i:i+5] for i in range(0, len(genre_data), 5)]
        
        chunk_seq_start = time.time()
        chunk_seq_results = [process_revenue_chunk(chunk) for chunk in chunks]
        chunk_seq_time = time.time() - chunk_seq_start
        
        chunk_par_start = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            chunk_par_results = list(executor.map(process_revenue_chunk, chunks))
        chunk_par_time = time.time() - chunk_par_start
        
        chunk_speedup = chunk_seq_time / chunk_par_time if chunk_par_time > 0 else 0
        
        performance_stats = {
            'cpu_cores': cpu_cores,
            'total_items': len(test_ids),
            'sequential_time': round(seq_time, 4),
            'thread_2_time': round(thread_time_2, 4),
            'thread_4_time': round(thread_time_4, 4),
            'thread_8_time': round(thread_time_8, 4),
            'process_2_time': round(process_time_2, 4),
            'process_4_time': round(process_time_4, 4),
            'speedup_thread_2': round(speedup_thread_2, 2),
            'speedup_thread_4': round(speedup_thread_4, 2),
            'speedup_thread_8': round(speedup_thread_8, 2),
            'speedup_process_2': round(speedup_process_2, 2),
            'speedup_process_4': round(speedup_process_4, 2),
            'chunk_seq_time': round(chunk_seq_time, 4),
            'chunk_par_time': round(chunk_par_time, 4),
            'chunk_speedup': round(chunk_speedup, 2),
        }

        best_method = 'Sequential'
        best_time = seq_time
        
        if thread_time_4 < best_time:
            best_method = 'Threading (4 workers)'
            best_time = thread_time_4
        if process_time_2 < best_time:
            best_method = 'Multiprocessing (2 workers)'
            best_time = process_time_2
        if process_time_4 < best_time:
            best_method = 'Multiprocessing (4 workers)'
            best_time = process_time_4
        
        performance_stats['best_method'] = best_method
        performance_stats['best_time'] = round(best_time, 4)

        methods_comparison = [
            {'method': 'Послідовна обробка', 'time': seq_time, 'speedup': 1.0},
            {'method': 'Threading (2)', 'time': thread_time_2, 'speedup': speedup_thread_2},
            {'method': 'Threading (4)', 'time': thread_time_4, 'speedup': speedup_thread_4},
            {'method': 'Threading (8)', 'time': thread_time_8, 'speedup': speedup_thread_8},
            {'method': 'Multiprocessing (2)', 'time': process_time_2, 'speedup': speedup_process_2},
            {'method': 'Multiprocessing (4)', 'time': process_time_4, 'speedup': speedup_process_4},
        ]
        
        context = {
            'performance_stats': performance_stats,
            'methods_comparison': methods_comparison,
        }
        
        return render(request, 'analytics/parallel_dashboard.html', context)
        
    except Exception as e:
        context = {
            'error': f'Помилка при тестуванні продуктивності: {str(e)}'
        }
        return render(request, 'analytics/parallel_dashboard.html', context)


if __name__ == '__main__':
    freeze_support()