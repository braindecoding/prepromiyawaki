#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create sharp datasets for Conditions 2, 3, 4, 5 (geometrical figures and alphabet letters)
With homogeneous filtering and integer scaling for maximum sharpness
"""

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

def resize_sharp_integer_scaling(img_10x10):
    """
    Resize 10x10 to 28x28 using integer scaling for maximum sharpness
    """
    # Scale by exactly 3x (10x10 -> 30x30)
    img_30x30 = np.repeat(np.repeat(img_10x10, 3, axis=0), 3, axis=1)
    
    # Crop to 28x28 (remove 1 pixel from each edge)
    img_28x28 = img_30x30[1:29, 1:29]
    
    return img_28x28

def filter_homogeneous_stimuli(pixel_values, threshold_variance=0.01, threshold_range=0.1):
    """
    Filter out homogeneous stimuli based on variance and range
    """
    n_samples = pixel_values.shape[0]
    variances = np.var(pixel_values, axis=1)
    ranges = np.max(pixel_values, axis=1) - np.min(pixel_values, axis=1)
    
    # Create mask for stimuli to keep
    variance_mask = variances > threshold_variance
    range_mask = ranges > threshold_range
    keep_mask = variance_mask & range_mask
    
    return keep_mask, variances, ranges

def create_condition_dataset(input_file, output_file, condition_number,
                           threshold_variance=0.01, threshold_range=0.1,
                           target_train_size=150, target_test_size=18):
    """
    Create sharp dataset for a specific condition
    """
    
    condition_descriptions = {
        2: "Geometrical figures",
        3: "Alphabet letters-1A", 
        4: "Alphabet letters-1B",
        5: "Alphabet letters-2"
    }
    
    condition_sessions = {
        2: [21, 22, 23, 24],
        3: [25, 26],
        4: [27, 28], 
        5: [29, 30, 31, 32]
    }
    
    print(f"=" * 70)
    print(f"CREATING CONDITION {condition_number} SHARP DATASET")
    print(f"Description: {condition_descriptions[condition_number]}")
    print(f"Sessions: {condition_sessions[condition_number]}")
    print(f"=" * 70)
    
    # Load original data
    print(f"\n📂 Loading original data...")
    data = sio.loadmat(input_file)
    mdata = data['D'][0,0]
    
    design = mdata['design']
    labels = mdata['label'] 
    fmri_data = mdata['data']
    
    session_numbers = design[:, 0]
    condition_codes = design[:, 2]
    
    # Filter for specific condition
    print(f"🔍 Filtering for Condition {condition_number}...")
    condition_mask = condition_codes == condition_number
    
    labels_filtered = labels[condition_mask]
    fmri_filtered = fmri_data[condition_mask]
    session_filtered = session_numbers[condition_mask]
    
    print(f"✅ Condition {condition_number} data:")
    print(f"   Total trials: {fmri_filtered.shape[0]}")
    print(f"   Sessions: {np.unique(session_filtered)}")
    print(f"   Expected sessions: {condition_sessions[condition_number]}")
    
    # Extract stimulus data
    pixel_values = labels_filtered[:, 1:101]  # 10x10 = 100 pixels
    stimulus_ids = labels_filtered[:, 0]
    
    print(f"\n🎨 Stimulus data:")
    print(f"   Shape: {pixel_values.shape}")
    print(f"   Unique stimuli: {len(np.unique(stimulus_ids))}")
    print(f"   Range: [{pixel_values.min():.3f}, {pixel_values.max():.3f}]")
    
    # Filter homogeneous stimuli
    print(f"\n🚫 Filtering homogeneous stimuli...")
    keep_mask, variances, ranges = filter_homogeneous_stimuli(
        pixel_values, threshold_variance, threshold_range
    )
    
    print(f"✅ Filtering results:")
    print(f"   Original: {len(pixel_values)}")
    print(f"   Filtered out: {np.sum(~keep_mask)} ({np.sum(~keep_mask)/len(pixel_values)*100:.1f}%)")
    print(f"   Kept: {np.sum(keep_mask)} ({np.sum(keep_mask)/len(pixel_values)*100:.1f}%)")
    
    if np.sum(keep_mask) == 0:
        print(f"❌ No stimuli passed filtering! Lowering thresholds...")
        # Lower thresholds for structured stimuli
        keep_mask, variances, ranges = filter_homogeneous_stimuli(
            pixel_values, threshold_variance=0.005, threshold_range=0.05
        )
        print(f"✅ With lower thresholds - Kept: {np.sum(keep_mask)}")
    
    # Apply filtering
    pixel_values_filtered = pixel_values[keep_mask]
    fmri_final = fmri_filtered[keep_mask]
    session_final = session_filtered[keep_mask]
    stimulus_ids_final = stimulus_ids[keep_mask]
    
    print(f"\n✅ After filtering: {fmri_final.shape[0]} samples available")
    
    # Check sample count and adjust if needed
    total_needed = target_train_size + target_test_size
    if fmri_final.shape[0] < total_needed:
        print(f"⚠️  Only {fmri_final.shape[0]} samples available, need {total_needed}")
        print(f"   Adjusting target sizes proportionally...")
        ratio = fmri_final.shape[0] / total_needed
        target_train_size = int(target_train_size * ratio)
        target_test_size = int(target_test_size * ratio)
        print(f"   New targets: train={target_train_size}, test={target_test_size}")
    
    # Resize using sharp integer scaling
    print(f"\n🔄 Resizing 10x10 to 28x28 using sharp integer scaling...")
    stimuli_resized = np.zeros((pixel_values_filtered.shape[0], 28*28))
    
    for i in range(pixel_values_filtered.shape[0]):
        img_10x10 = pixel_values_filtered[i].reshape(10, 10)
        img_28x28 = resize_sharp_integer_scaling(img_10x10)
        stimuli_resized[i] = img_28x28.flatten()
    
    print(f"✅ Resized stimuli: {stimuli_resized.shape}")
    
    # Normalize
    stimuli_processed = stimuli_resized / stimuli_resized.max()
    print(f"✅ Normalized range: [{stimuli_processed.min():.3f}, {stimuli_processed.max():.3f}]")
    
    # Process fMRI
    print(f"\n🧠 Processing fMRI data...")
    fmri_mean = fmri_final.mean(axis=0)
    fmri_std = fmri_final.std(axis=0)
    fmri_standardized = (fmri_final - fmri_mean) / fmri_std
    fmri_standardized = np.nan_to_num(fmri_standardized)
    
    # Create labels using session numbers
    labels_processed = session_final.reshape(-1, 1)
    
    # Split data
    print(f"\n✂️  Splitting data...")
    np.random.seed(42)
    total_samples = fmri_standardized.shape[0]
    indices = np.random.permutation(total_samples)
    
    train_indices = indices[:target_train_size]
    test_indices = indices[target_train_size:target_train_size + target_test_size]
    
    # Extract final data
    stimTrn = stimuli_processed[train_indices]
    fmriTrn = fmri_standardized[train_indices]
    labelTrn = labels_processed[train_indices]
    
    stimTest = stimuli_processed[test_indices]
    fmriTest = fmri_standardized[test_indices]
    labelTest = labels_processed[test_indices]
    
    print(f"\n🎯 FINAL CONDITION {condition_number} DATASET:")
    print(f"✅ fmriTrn: {fmriTrn.shape}")
    print(f"✅ stimTrn: {stimTrn.shape}")
    print(f"✅ fmriTest: {fmriTest.shape}")
    print(f"✅ stimTest: {stimTest.shape}")
    print(f"✅ labelTrn: {labelTrn.shape}")
    print(f"✅ labelTest: {labelTest.shape}")
    
    # Show session distribution
    train_sessions = np.unique(labelTrn.flatten())
    test_sessions = np.unique(labelTest.flatten())
    
    print(f"\n📋 Session distribution:")
    print(f"   Training sessions: {train_sessions}")
    print(f"   Test sessions: {test_sessions}")
    
    # Save dataset
    output_data = {
        'fmriTrn': fmriTrn,
        'stimTrn': stimTrn,
        'fmriTest': fmriTest,
        'stimTest': stimTest,
        'labelTrn': labelTrn,
        'labelTest': labelTest,
        'train_indices': train_indices,
        'test_indices': test_indices,
        'metadata': {
            'condition': condition_number,
            'description': condition_descriptions[condition_number],
            'sessions': condition_sessions[condition_number],
            'resize_method': 'integer_scaling',
            'original_samples': len(pixel_values),
            'filtered_samples': len(pixel_values_filtered),
            'threshold_variance': threshold_variance,
            'threshold_range': threshold_range,
            'train_sessions': train_sessions,
            'test_sessions': test_sessions,
            'unique_stimuli': len(np.unique(stimulus_ids_final))
        }
    }
    
    sio.savemat(output_file, output_data)
    print(f"\n✅ Dataset saved to: {output_file}")
    
    return output_data

def create_combined_conditions_2to5(input_file, output_file,
                                  threshold_variance=0.01, threshold_range=0.1,
                                  target_train_size=150, target_test_size=18):
    """
    Create combined dataset for Conditions 2, 3, 4, 5
    """
    
    print(f"=" * 70)
    print(f"CREATING COMBINED CONDITIONS 2-5 SHARP DATASET")
    print(f"Including: Geometrical figures + All alphabet letters")
    print(f"=" * 70)
    
    # Load original data
    print(f"\n📂 Loading original data...")
    data = sio.loadmat(input_file)
    mdata = data['D'][0,0]
    
    design = mdata['design']
    labels = mdata['label'] 
    fmri_data = mdata['data']
    
    session_numbers = design[:, 0]
    condition_codes = design[:, 2]
    
    # Filter for conditions 2, 3, 4, 5
    target_conditions = [2, 3, 4, 5]
    print(f"🔍 Filtering for conditions: {target_conditions}")
    condition_mask = np.isin(condition_codes, target_conditions)
    
    labels_filtered = labels[condition_mask]
    fmri_filtered = fmri_data[condition_mask]
    session_filtered = session_numbers[condition_mask]
    condition_filtered = condition_codes[condition_mask]
    
    print(f"✅ Combined conditions data:")
    print(f"   Total trials: {fmri_filtered.shape[0]}")
    print(f"   Sessions: {np.unique(session_filtered)}")
    print(f"   Conditions: {np.unique(condition_filtered)}")
    
    # Extract stimulus data
    pixel_values = labels_filtered[:, 1:101]
    stimulus_ids = labels_filtered[:, 0]
    
    # Filter homogeneous stimuli
    print(f"\n🚫 Filtering homogeneous stimuli...")
    keep_mask, variances, ranges = filter_homogeneous_stimuli(
        pixel_values, threshold_variance, threshold_range
    )
    
    print(f"✅ Filtering results:")
    print(f"   Original: {len(pixel_values)}")
    print(f"   Kept: {np.sum(keep_mask)} ({np.sum(keep_mask)/len(pixel_values)*100:.1f}%)")
    
    # Apply filtering
    pixel_values_filtered = pixel_values[keep_mask]
    fmri_final = fmri_filtered[keep_mask]
    session_final = session_filtered[keep_mask]
    condition_final = condition_filtered[keep_mask]
    
    # Resize using sharp integer scaling
    print(f"\n🔄 Resizing with sharp integer scaling...")
    stimuli_resized = np.zeros((pixel_values_filtered.shape[0], 28*28))
    
    for i in range(pixel_values_filtered.shape[0]):
        img_10x10 = pixel_values_filtered[i].reshape(10, 10)
        img_28x28 = resize_sharp_integer_scaling(img_10x10)
        stimuli_resized[i] = img_28x28.flatten()
    
    # Normalize and process
    stimuli_processed = stimuli_resized / stimuli_resized.max()
    
    fmri_mean = fmri_final.mean(axis=0)
    fmri_std = fmri_final.std(axis=0)
    fmri_standardized = (fmri_final - fmri_mean) / fmri_std
    fmri_standardized = np.nan_to_num(fmri_standardized)
    
    # Use condition numbers as labels instead of session numbers
    labels_processed = condition_final.reshape(-1, 1)
    
    # Adjust target sizes if needed
    total_needed = target_train_size + target_test_size
    if fmri_standardized.shape[0] < total_needed:
        ratio = fmri_standardized.shape[0] / total_needed
        target_train_size = int(target_train_size * ratio)
        target_test_size = int(target_test_size * ratio)
    
    # Stratified split by condition to ensure balanced test set
    print(f"\n✂️  Creating stratified split by condition...")
    np.random.seed(42)

    # Calculate samples per condition for test set
    unique_conditions = np.unique(condition_final)
    n_conditions = len(unique_conditions)
    test_per_condition = target_test_size // n_conditions
    remaining_test = target_test_size % n_conditions

    print(f"📊 Test set distribution strategy:")
    print(f"   Target test size: {target_test_size}")
    print(f"   Conditions: {unique_conditions}")
    print(f"   Base samples per condition: {test_per_condition}")
    print(f"   Extra samples to distribute: {remaining_test}")

    train_indices = []
    test_indices = []

    for i, condition in enumerate(unique_conditions):
        condition_mask = condition_final == condition
        condition_indices = np.where(condition_mask)[0]

        # Calculate test samples for this condition
        test_samples_this_condition = test_per_condition
        if i < remaining_test:  # Distribute remaining samples to first conditions
            test_samples_this_condition += 1

        print(f"   Condition {condition}: {len(condition_indices)} total → {test_samples_this_condition} test")

        # Randomly select test samples for this condition
        np.random.shuffle(condition_indices)
        condition_test_indices = condition_indices[:test_samples_this_condition]
        condition_train_indices = condition_indices[test_samples_this_condition:]

        test_indices.extend(condition_test_indices)
        train_indices.extend(condition_train_indices)

    # Convert to numpy arrays
    train_indices = np.array(train_indices)
    test_indices = np.array(test_indices)

    # Adjust train size if needed
    if len(train_indices) > target_train_size:
        np.random.shuffle(train_indices)
        train_indices = train_indices[:target_train_size]

    print(f"✅ Final split:")
    print(f"   Train samples: {len(train_indices)}")
    print(f"   Test samples: {len(test_indices)}")

    # Verify test set distribution
    test_conditions = condition_final[test_indices]
    for condition in unique_conditions:
        count = np.sum(test_conditions == condition)
        print(f"   Test condition {condition}: {count} samples")
    
    # Extract final data
    stimTrn = stimuli_processed[train_indices]
    fmriTrn = fmri_standardized[train_indices]
    labelTrn = labels_processed[train_indices]

    stimTest = stimuli_processed[test_indices]
    fmriTest = fmri_standardized[test_indices]
    labelTest = labels_processed[test_indices]

    print(f"\n🎯 FINAL COMBINED DATASET:")
    print(f"✅ fmriTrn: {fmriTrn.shape}")
    print(f"✅ stimTrn: {stimTrn.shape}")
    print(f"✅ fmriTest: {fmriTest.shape}")
    print(f"✅ stimTest: {stimTest.shape}")
    print(f"✅ labelTrn: {labelTrn.shape}")
    print(f"✅ labelTest: {labelTest.shape}")

    # Show final condition distribution
    print(f"\n📊 Final condition distribution:")
    train_conditions = labelTrn.flatten()
    test_conditions = labelTest.flatten()

    print(f"   Training set:")
    for condition in unique_conditions:
        count = np.sum(train_conditions == condition)
        print(f"     Condition {condition}: {count} samples")

    print(f"   Test set:")
    for condition in unique_conditions:
        count = np.sum(test_conditions == condition)
        print(f"     Condition {condition}: {count} samples")
    
    # Save dataset
    output_data = {
        'fmriTrn': fmriTrn,
        'stimTrn': stimTrn,
        'fmriTest': fmriTest,
        'stimTest': stimTest,
        'labelTrn': labelTrn,
        'labelTest': labelTest,
        'train_indices': train_indices,
        'test_indices': test_indices,
        'metadata': {
            'conditions': target_conditions,
            'description': 'Combined Conditions 2-5: Geometrical figures + Alphabet letters',
            'resize_method': 'integer_scaling',
            'original_samples': len(pixel_values),
            'filtered_samples': len(pixel_values_filtered),
            'threshold_variance': threshold_variance,
            'threshold_range': threshold_range,
            'split_method': 'stratified_by_condition',
            'test_distribution': {int(cond): int(np.sum(labelTest.flatten() == cond))
                               for cond in unique_conditions},
            'train_distribution': {int(cond): int(np.sum(labelTrn.flatten() == cond))
                                 for cond in unique_conditions}
        }
    }
    
    sio.savemat(output_file, output_data)
    print(f"\n✅ Combined dataset saved to: {output_file}")
    
    return output_data

def main():
    """
    Create all condition datasets with sharp integer scaling
    """
    input_file = 'data/de_s1_V1_Ecc1to11_baseByRestPre_smlr_s1071119ROI_resol10_leave0_1x1_preprocessed.mat'
    
    print("🚀 CREATING SHARP DATASETS FOR CONDITIONS 2-5")
    print("📋 Will create:")
    print("   1. Individual datasets for each condition (2, 3, 4, 5)")
    print("   2. Combined dataset for all conditions 2-5")
    print("   3. All with sharp integer scaling and homogeneous filtering")
    
    # Create individual condition datasets
    conditions = [2, 3, 4, 5]
    condition_names = {
        2: "geometrical",
        3: "alphabet_1a", 
        4: "alphabet_1b",
        5: "alphabet_2"
    }
    
    for condition in conditions:
        print(f"\n" + "=" * 50)
        print(f"CREATING CONDITION {condition} DATASET")
        print("=" * 50)
        
        output_file = f'data/miyawaki_condition{condition}_{condition_names[condition]}_sharp.mat'
        
        try:
            create_condition_dataset(
                input_file=input_file,
                output_file=output_file,
                condition_number=condition,
                threshold_variance=0.01,
                threshold_range=0.1,
                target_train_size=150,
                target_test_size=18
            )
        except Exception as e:
            print(f"❌ Error creating condition {condition}: {e}")
    
    # Create combined dataset
    print(f"\n" + "=" * 50)
    print("CREATING COMBINED CONDITIONS 2-5 DATASET")
    print("=" * 50)
    
    try:
        create_combined_conditions_2to5(
            input_file=input_file,
            output_file='data/miyawaki_conditions_2to5_combined_sharp.mat',
            threshold_variance=0.01,
            threshold_range=0.1,
            target_train_size=150,
            target_test_size=18
        )
    except Exception as e:
        print(f"❌ Error creating combined dataset: {e}")
    
    print(f"\n" + "=" * 70)
    print("🎉 ALL CONDITION DATASETS CREATED!")
    print("=" * 70)
    print("Generated files:")
    print("  1. miyawaki_condition2_geometrical_sharp.mat")
    print("  2. miyawaki_condition3_alphabet_1a_sharp.mat") 
    print("  3. miyawaki_condition4_alphabet_1b_sharp.mat")
    print("  4. miyawaki_condition5_alphabet_2_sharp.mat")
    print("  5. miyawaki_conditions_2to5_combined_sharp.mat")
    print("\n✅ All datasets use sharp integer scaling and homogeneous filtering!")

if __name__ == "__main__":
    main()
