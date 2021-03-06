import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  
  for i in range(num_train):
    scores = X[i].dot(W)
    correct_class_score = scores[y[i]]
    num_correct_class_score = 0
    for j in range(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        dW[:, j] += X[i]
        num_correct_class_score += 1
    dW[:,y[i]] += -1*num_correct_class_score*X[i]

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW /= num_train
  
  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  #backprop regularisation
  dW += 2*reg*W
  
  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]
  scores = X@W #(N,C)
  correct_class_score = scores[np.arange(num_train), y]
  
  #Don't count in loss if j = y[i]
  mask = np.ones((num_train, num_classes))
  #if j = y[i] mask[i,j] := 0
  np.put_along_axis(mask, y[:, None], 0, axis=1)
  
  margins = mask * np.maximum(scores - correct_class_score[:, None] + 1, 0)
  loss = np.sum(margins)/num_train

  # Add regularization to the loss.
  loss += reg * np.sum(W * W) 


  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  id_dW = 1 * (margins > 0)
  num_correct_class = np.sum(id_dW, axis=1)
  id_dW[np.arange(num_train), y] = - num_correct_class
  dW = X.T@id_dW
  
  dW /= num_train
  dW += 2*reg*W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
